// JavaScript/ipcHandlers.js

/*
 * Módulo que registra handlers IPC (ipcMain) usados por la UI (renderer) para
 * interactuar con el proceso principal.
 *
 * Canales principales:
 *  - 'open-media-dialog' (ipcMain.handle): abre diálogo de selección de archivos
 *      Input: maxFiles (number) -> si >1 activa multiSelections
 *      Output: array de paths o null si cancelado
 *
 *  - 'selection-made' (ipcMain.on): evento que contiene la configuración final
 *      Payload esperado: { size, position, mediaFiles, distributionScheme, assignmentMap }
 *      - size: '1'|'2'|'3' (quarter/half/full)
 *      - position: string (índice 1..4)
 *      - mediaFiles: array de rutas absolutas
 *      - distributionScheme: string identificador (none/three_individual/one_big/two_halves)
 *      - assignmentMap: objeto con asignaciones específicas para modos avanzados
 *
 * Implementación nota:
 *  - Para distribuciones que fusionan regiones se usan índices especiales: 98 y 99
 *    (98: fusion avanzado 'two_halves', 99: 'one_big' que fusiona las 3 areas restantes)
 */

const { ipcMain, dialog, BrowserWindow } = require('electron');
const fs = require('fs');
const path = require('path');

// Módulos propios
const appState = require('./appState');
const pathManager = require('./pathManager');
const configManager = require('./configManager');
const windowManager = require('./windowManager');
const inactivityManager = require('./inactivityManager');
const { calculatePositions } = require('./positionCalculator');

function registerHandlers() {

    // ----------------------
    // Handler: abrir diálogo de selección de archivos
    // - Usa pathManager.resourcesDir como defaultPath
    // - Devuelve array de rutas, o null si el usuario cancela
    // ----------------------
    ipcMain.handle('open-media-dialog', async (event, maxFiles) => {
        const window = BrowserWindow.fromWebContents(event.sender);
        
        const properties = ['openFile'];
        if (maxFiles > 1) {
            properties.push('multiSelections');
        }

        const result = await dialog.showOpenDialog(window, {
            properties: properties,
            filters: [
                { name: 'Media', extensions: ['png', 'jpg', 'jpeg', 'gif', 'webp', 'mp4'] }
            ],
            message: `Selecciona hasta ${maxFiles} archivos de imagen o video.`,
            defaultPath: pathManager.resourcesDir 
        });

        if (result.canceled) {
            return null;
        }
        return result.filePaths;
    });

    // ----------------------
    // Evento: crear ventanas y cargar contenido según la selección
    // ----------------------
    ipcMain.on('selection-made', (e, { size, position, mediaFiles, distributionScheme, assignmentMap }) => {
        
        try {
            console.log('[SELECCION] Recibido:', { size, position, mediaFiles, distributionScheme, assignmentMap });
            
            // Cerrar ventanas anteriores y resetear timers
            windowManager.closeAllWindows();
            inactivityManager.clearInactivityTimer();

            // Calcular bounds para la ventana principal y las de fondo
            const { mainBounds, otherBounds } = calculatePositions(size, parseInt(position));

            let finalOtherBounds = otherBounds;
            let userMediaMap = {};
            
            // --- LÓGICA DE DISTRIBUCIÓN AVANZADA ---
            if (size === '1') {
                const remainingBounds = otherBounds; 
                
                if (distributionScheme === 'one_big' && mediaFiles.length >= 1) {
                    // Fusiona las 3 areas restantes en una grande (index 99)
                    const minX = Math.min(...remainingBounds.map(b => b.x));
                    const minY = Math.min(...remainingBounds.map(b => b.y));
                    const maxX = Math.max(...remainingBounds.map(b => b.x + b.width));
                    const maxY = Math.max(...remainingBounds.map(b => b.y + b.height));

                    const combinedBounds = { x: minX, y: minY, width: maxX - minX, height: maxY - minY, index: 99 };
                    finalOtherBounds = [combinedBounds];
                    userMediaMap[99] = mediaFiles[0];

                    console.log('[FUSIONADO] Fundo unico creado:', combinedBounds);
                    console.log('[FUSIONADO] Archivo asignado:', mediaFiles[0]);

                } else if (distributionScheme === 'three_individual' && mediaFiles.length >= 3) {
                    // Asignación 1:1 a las 3 areas restantes
                    finalOtherBounds = remainingBounds;
                    remainingBounds.forEach((bounds, idx) => {
                         userMediaMap[bounds.index] = mediaFiles[idx];
                         console.log(`[INDIVIDUAL] Asignado archivo ${idx} (${mediaFiles[idx]}) a index ${bounds.index}`);
                    });

                } else if (distributionScheme === 'none') {
                     finalOtherBounds = [];
                
                } else if (distributionScheme === 'two_halves' && mediaFiles.length >= 2) {
                    // Fusionar dos areas y dejar una individual (index 98 para fusionadas)
                    const individualIndex = parseInt(assignmentMap.individualArea); 
                    const boundsToFuse = remainingBounds.filter(b => b.index !== individualIndex);
                    const individualBound = remainingBounds.find(b => b.index === individualIndex);
                    
                    const minX = Math.min(...boundsToFuse.map(b => b.x));
                    const minY = Math.min(...boundsToFuse.map(b => b.y));
                    const maxX = Math.max(...boundsToFuse.map(b => b.x + b.width));
                    const maxY = Math.max(...boundsToFuse.map(b => b.y + b.height));
                    
                    const combinedBounds = { x: minX, y: minY, width: maxX - minX, height: maxY - minY, index: 98 };
                    
                    finalOtherBounds = [combinedBounds, individualBound];
                    
                    userMediaMap[98] = mediaFiles[0]; 
                    userMediaMap[individualBound.index] = mediaFiles[1]; 
                    
                    console.log('[FUSIONADO AVANZADO] Bounds fusionados:', combinedBounds);
                    console.log('[FUSIONADO AVANZADO] Archivo fusionado:', mediaFiles[0]);
                    console.log('[FUSIONADO AVANZADO] Bound individual:', individualBound);
                    console.log('[FUSIONADO AVANZADO] Archivo individual:', mediaFiles[1]);
                }
            } else if (size === '2' && mediaFiles.length >= 1) {
                // LÓGICA PARA 1/2 PANTALLA: asignar primer media al fondo disponible
                if (otherBounds.length > 0) {
                    finalOtherBounds = otherBounds;
                    userMediaMap[otherBounds[0].index] = mediaFiles[0];
                    console.log('[MITAD PANTALLA] Archivo asignado a ventana de fondo:', {
                        index: otherBounds[0].index,
                        file: mediaFiles[0]
                    });
                }
            } else if (size === '3') {
                // Pantalla completa no tiene fondos
                finalOtherBounds = [];
            }

            console.log('[DEBUG] userMediaMap final:', userMediaMap);
            console.log('[DEBUG] finalOtherBounds:', finalOtherBounds);

            // Cerrar selector si está abierto
            if (appState.winSelector) {
                appState.winSelector.close();
                appState.winSelector = null;
            }

            // 1. Crear ventana principal
            const mainWin = windowManager.createWindow(mainBounds, true);
            appState.windows.push(mainWin);
            
            // 2. Crear ventanas de fondo según finalOtherBounds
            finalOtherBounds.forEach((bounds) => {
                const bgWin = windowManager.createWindow(bounds, false);
                appState.windows.push(bgWin);
            });
            
            // Guardar la configuración para posible re-aplicación al iniciar
            configManager.saveLastConfig({ 
                size, 
                position, 
                mediaFiles, 
                distributionScheme, 
                assignmentMap 
            });

            // ----------------------
            // Al cargar la ventana principal: inicializar watcher y enviar datos al renderer
            // ----------------------
            mainWin.webContents.once('did-finish-load', () => {
                
                const { 
                    bannersTopPath, 
                    bannersBottomPath, 
                    mobileImgsPath,
                    userFile,
                    welcomeImage,
                    resourcesDir,
                    getFileUrl
                } = pathManager;

                const config = configManager.getConfig();
                
                const bannersTop = fs.existsSync(bannersTopPath) 
                    ? fs.readdirSync(bannersTopPath)
                        .filter(f => /\.(png|jpe?g|gif|webp)$/i.test(f))
                        .map(f => getFileUrl(path.join(bannersTopPath,f))) 
                    : [];
                const bannersBottom = fs.existsSync(bannersBottomPath) 
                    ? fs.readdirSync(bannersBottomPath)
                        .filter(f => /\.(png|jpe?g|gif|webp)$/i.test(f))
                        .map(f => getFileUrl(path.join(bannersBottomPath,f))) 
                    : [];
                const mobileImgs = fs.existsSync(mobileImgsPath) 
                    ? fs.readdirSync(mobileImgsPath)
                        .filter(f => /\.(png|jpe?g|gif|webp)$/i.test(f))
                        .map(f => getFileUrl(path.join(mobileImgsPath,f))) 
                    : [];

                // Vigilar cambios en el directorio de recursos para reaccionar ante actualizaciones
                const watcher = fs.watch(resourcesDir, (eventType, filename) => {
                    if (filename === config.userFileName) { 
                        
                        inactivityManager.startInactivityTimer(mainWin); 

                        if (!fs.existsSync(userFile)) {
                            mainWin.webContents.send('no-file', { 
                                welcomePath: getFileUrl(welcomeImage) 
                            });
                        } else if (eventType === 'change') {
                            const text = fs.readFileSync(userFile, 'utf-8');
                            mainWin.webContents.send('file-changed', text);
                            
                            mainWin.webContents.send('load-images', {
                                bannersTop,
                                bannersBottom,
                                mobileImgs,
                                mediaFiles: []
                            });
                        }
                    }
                });

                mainWin.on('closed', () => {
                    watcher.close();
                    inactivityManager.clearInactivityTimer();
                    windowManager.closeAllWindows(); // Cierra todas las demás ventanas (fondo)
                });

                // Carga inicial: si existe userFile, enviarlo; si no, enviar bienvenida
                console.log(`[DIAGNOSTICO] Verificando archivo de usuario en: ${userFile}`); 
                if (fs.existsSync(userFile)) {
                    console.log('[DIAGNOSTICO] Archivo encontrado. Cargando contenido.'); 
                    const text = fs.readFileSync(userFile, 'utf-8');
                    mainWin.webContents.send('file-changed', text);
                    inactivityManager.startInactivityTimer(mainWin); 
                } else {
                    console.log(`[DIAGNOSTICO] Archivo NO encontrado. Cargando Bienvenida desde: ${getFileUrl(welcomeImage)}`);
                    mainWin.webContents.send('no-file', { 
                        welcomePath: getFileUrl(welcomeImage) 
                    });
                }
                
                mainWin.webContents.send('window-size-selected', { size: size });
                
                mainWin.webContents.send('load-images', {
                    bannersTop,
                    bannersBottom,
                    mobileImgs,
                    mediaFiles: [] 
                });

                // Cargar medios en ventanas de fondo
                const bgWindows = appState.windows.filter(w => w !== mainWin);
                
                console.log(`[DEBUG] Total de ventanas de fondo: ${bgWindows.length}`);
                
                bgWindows.forEach((bgWin, winIdx) => {
                    console.log(`[DEBUG] Procesando ventana de fondo ${winIdx + 1}`);
                    
                    bgWin.webContents.once('did-finish-load', () => {
                        const positionIndex = bgWin.positionIndex;
                        const mediaFilePath = userMediaMap[positionIndex];
                        
                        console.log(`[VENTANA FONDO] Index ${positionIndex} - Archivo: ${mediaFilePath}`);
                        
                        if (mediaFilePath) {
                            if (!fs.existsSync(mediaFilePath)) {
                                console.error(`[ERROR] El archivo NO existe: ${mediaFilePath}`);
                                return;
                            }
                            
                            console.log(`[OK] El archivo existe: ${mediaFilePath}`);
                            
                            const fileName = path.basename(mediaFilePath);
                            const isVideo = /\.(mp4)$/i.test(fileName);
                            const isGif = /\.(gif)$/i.test(fileName);
                            
                            const normalizedPath = path.normalize(mediaFilePath);
                            const mediaUrl = getFileUrl(normalizedPath);
                            
                            const mediaForWindow = {
                                type: isVideo ? 'video' : isGif ? 'gif' : 'image',
                                src: mediaUrl,
                                name: fileName,
                                priority: positionIndex
                            };

                            console.log(`[ENVIANDO MEDIA] A ventana index ${positionIndex}:`, mediaForWindow);

                            bgWin.webContents.send('load-images', {
                                mediaFiles: [mediaForWindow]
                            });
                        } else {
                            console.log(`[VENTANA FONDO] Index ${positionIndex} - Sin archivo asignado.`);
                        }
                    });
                });
            });

        } catch (error) {
            // En caso de error, volvemos al selector para permitir al usuario reintentar
            console.error('[FATAL CRASH] Error al procesar la configuración y crear ventanas.', error.message, error.stack);
            
            windowManager.closeAllWindows();
            windowManager.createSelectorWindow();
        }
    });
}

module.exports = {
    registerHandlers
};