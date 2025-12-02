// JavaScript/ipcHandlers.js (CORREGIDO Y COMPLETO)

const { ipcMain, dialog, BrowserWindow } = require('electron');
const fs = require('fs');
const path = require('path');

// Importación de módulos internos
const appState = require('./appState');
const pathManager = require('./pathManager'); 
const configManager = require('./configManager');
const windowManager = require('./windowManager');
const inactivityManager = require('./inactivityManager');
const { calculatePositions } = require('./positionCalculator');
const logManager = require('./logManager'); 

function registerHandlers() {

    // ----------------------
    // HANDLER 1: Diálogo de Selección de Archivos
    // Permite al usuario buscar imágenes/videos en su disco local.
    // ----------------------
    ipcMain.handle('open-media-dialog', async (event, maxFiles) => {
        const window = BrowserWindow.fromWebContents(event.sender);
        
        const properties = ['openFile'];
        if (maxFiles > 1) {
            properties.push('multiSelections'); // Habilita selección múltiple si se requiere
        }

        const result = await dialog.showOpenDialog(window, {
            properties: properties,
            filters: [
                { name: 'Media', extensions: ['png', 'jpg', 'jpeg', 'gif', 'webp', 'mp4'] }
            ],
            message: `Selecciona hasta ${maxFiles} archivos de imagen o video.`,
            defaultPath: pathManager.resourcesDir // Abre por defecto en la carpeta de recursos
        });

        if (result.canceled) {
            return null;
        }
        return result.filePaths;
    });

    // ----------------------
    // HANDLER 2: Procesar Selección (CORE LOGIC)
    // Recibe configuración, calcula posiciones y crea las ventanas.
    // ----------------------
    ipcMain.on('selection-made', (e, selectionData) => {
        // Desestructuramos para tener las variables disponibles como antes
        const { size, position, mediaFiles, distributionScheme, assignmentMap } = selectionData;
        
        try {
            logManager.log('INFO', 'SELECTION_RECEIVED', `Nueva selección: Tamaño=${size}, Posición=${position}, Archivos=${mediaFiles.length}`); 
            console.log('[SELECCION] Recibido:', { size, position, mediaFiles, distributionScheme, assignmentMap });
            
            // =================================================================================
            // [CAMBIO IMPORTANTE] GUARDAR CONFIGURACIÓN AHORA MISMO
            // Lo hacemos al principio para asegurar que se guarde aunque fallen las ventanas después.
            // =================================================================================
            configManager.saveLastConfig(selectionData);
            console.log('[IPC] Configuración guardada preventivamente.');

            // Limpieza previa: cerrar ventanas anteriores y limpiar timers
            windowManager.closeAllWindows();
            inactivityManager.clearInactivityTimer();

            // Calculamos geometría de ventanas
            const { mainBounds, otherBounds } = calculatePositions(size, parseInt(position));

            let finalOtherBounds = otherBounds;
            let userMediaMap = {};
            
            // --- LÓGICA DE DISTRIBUCIÓN AVANZADA (Fusión de cuadrantes) ---
            if (size === '1') { // Caso 1/4 de pantalla
                const remainingBounds = otherBounds; 
                
                // Esquema: Una imagen grande ocupando el espacio restante (forma de L invertida)
                if (distributionScheme === 'one_big' && mediaFiles.length >= 1) {
                    const minX = Math.min(...remainingBounds.map(b => b.x));
                    const minY = Math.min(...remainingBounds.map(b => b.y));
                    const maxX = Math.max(...remainingBounds.map(b => b.x + b.width));
                    const maxY = Math.max(...remainingBounds.map(b => b.y + b.height));

                    // Creamos un súper-bounds que cubre los 3 cuadrantes restantes
                    const combinedBounds = { x: minX, y: minY, width: maxX - minX, height: maxY - minY, index: 99 };
                    finalOtherBounds = [combinedBounds];
                    userMediaMap[99] = mediaFiles[0];

                } else if (distributionScheme === 'three_individual' && mediaFiles.length >= 3) {
                    // Esquema: 3 imágenes distintas en los 3 cuadrantes restantes
                    finalOtherBounds = remainingBounds;
                    remainingBounds.forEach((bounds, idx) => {
                         userMediaMap[bounds.index] = mediaFiles[idx];
                    });

                } else if (distributionScheme === 'none') {
                     // Sin fondo (negro)
                     finalOtherBounds = [];
                
                } else if (distributionScheme === 'two_halves' && mediaFiles.length >= 2) {
                    // Esquema híbrido: Un bloque doble y uno simple
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
                }
            } else if (size === '2' && mediaFiles.length >= 1) {
                // Caso 1/2 pantalla: La otra mitad es el fondo
                if (otherBounds.length > 0) {
                    finalOtherBounds = otherBounds;
                    userMediaMap[otherBounds[0].index] = mediaFiles[0];
                }
            } else if (size === '3') {
                // Pantalla completa no tiene fondos
                finalOtherBounds = [];
            }


            // Cerrar ventana del selector una vez configurado
            if (appState.winSelector) {
                appState.winSelector.close();
                appState.winSelector = null;
            }

            // 1. Crear ventana principal (VIDEO)
            const mainWin = windowManager.createWindow(mainBounds, true);
            appState.windows.push(mainWin);
            
            // 2. Crear ventanas de fondo (IMÁGENES)
            const bgWindows = [];
            finalOtherBounds.forEach((bounds) => {
                const bgWin = windowManager.createWindow(bounds, false);
                appState.windows.push(bgWin);
                bgWindows.push(bgWin); 
            });
            
            // NOTA: Ya hemos guardado la configuración al principio, así que borramos la llamada que había aquí abajo.
            logManager.log('INFO', 'WINDOWS_CREATED', `Ventanas principal y ${finalOtherBounds.length} de fondo creadas con éxito.`); 
            
            // ----------------------------------------------------
            // GESTIÓN DE LA VENTANA PRINCIPAL (Carga de assets)
            // ----------------------------------------------------
            mainWin.webContents.once('did-finish-load', () => {
                
                const config = configManager.getConfig();
                
                // Helper para cargar imágenes de directorios fijos (banners, etc.)
                const getMediaUrls = (dirPath) => {
                    if (fs.existsSync(dirPath)) {
                        return fs.readdirSync(dirPath)
                            .filter(f => /\.(png|jpe?g|gif|webp|mp4)$/i.test(f))
                            .map(f => pathManager.getFileUrl(path.join(dirPath, f)));
                    }
                    return [];
                };

                const bannersTop = getMediaUrls(pathManager.bannersTopPath);
                const bannersBottom = getMediaUrls(pathManager.bannersBottomPath);
                const mobileImgs = getMediaUrls(pathManager.mobileImgsPath);

                // Crear carpeta de recursos si no existe ANTES de hacer watch
                if (!fs.existsSync(pathManager.resourcesDir)) {
                    fs.mkdirSync(pathManager.resourcesDir, { recursive: true });
                    logManager.log('INFO', 'RESOURCES_DIR_CREATED', `Carpeta de recursos creada: ${pathManager.resourcesDir}`);
                }

                // WATCHER: Vigila cambios en 'contenido.txt'
                const watcher = fs.watch(pathManager.resourcesDir, (eventType, filename) => { 
                    if (filename === config.userFileName) { 
                        
                        // Reiniciar temporizador de inactividad con cada interacción
                        inactivityManager.startInactivityTimer(mainWin); 

                        if (!fs.existsSync(pathManager.userFile)) { 
                            // Si el archivo se borra, mostramos pantalla por defecto
                            mainWin.webContents.send('no-file', {});
                        } else if (eventType === 'change') {
                            // Si el archivo cambia, leemos y enviamos nuevo texto
                            const text = fs.readFileSync(pathManager.userFile, 'utf-8'); 
                            mainWin.webContents.send('file-changed', text);
                            
                            // Recargar imágenes para asegurar frescura
                            mainWin.webContents.send('load-images', {
                                bannersTop,
                                bannersBottom,
                                mobileImgs,
                                mediaFiles: []
                            });
                        }
                    }
                });

                // Limpieza al cerrar ventana
                mainWin.on('closed', () => {
                    watcher.close();
                    inactivityManager.clearInactivityTimer();
                    windowManager.closeAllWindows(); 
                });

                // Carga inicial al abrir
                if (fs.existsSync(pathManager.userFile)) { 
                    const text = fs.readFileSync(pathManager.userFile, 'utf-8'); 
                    mainWin.webContents.send('file-changed', text);
                    inactivityManager.startInactivityTimer(mainWin); 
                } else {
                    mainWin.webContents.send('no-file', {}); 
                }
                
                // Enviar datos de configuración a la vista
                mainWin.webContents.send('window-size-selected', { size: size });
                mainWin.webContents.send('load-images', {
                    bannersTop,
                    bannersBottom,
                    mobileImgs,
                    mediaFiles: [] 
                });
            });


            // -----------------------------------------------------------
            // GESTIÓN DE VENTANAS DE FONDO
            // -----------------------------------------------------------
            bgWindows.forEach((bgWin) => {
                
                bgWin.webContents.once('did-finish-load', () => {
                    const positionIndex = bgWin.positionIndex;
                    const mediaFilePath = userMediaMap[positionIndex];
                    
                    if (mediaFilePath && fs.existsSync(mediaFilePath)) {
                        
                        const fileName = path.basename(mediaFilePath);
                        const isVideo = /\.(mp4)$/i.test(fileName);
                        const isGif = /\.(gif)$/i.test(fileName);
                        
                        const normalizedPath = path.normalize(mediaFilePath);
                        
                        // Generamos URL segura (file://)
                        const mediaUrl = pathManager.getFileUrl(normalizedPath);
                        
                        const mediaForWindow = {
                            type: isVideo ? 'video' : isGif ? 'gif' : 'image',
                            src: mediaUrl,
                            name: fileName,
                            priority: positionIndex
                        };

                        // Enviamos la orden de renderizado al HTML de fondo
                        bgWin.webContents.send('load-images', {
                            mediaFiles: [mediaForWindow]
                        });
                    } else {
                         console.log(`[VENTANA FONDO] Index ${positionIndex} - Sin archivo asignado.`);
                         bgWin.webContents.send('load-images', { mediaFiles: [] });
                    }
                });
            });

        } catch (error) {
            // Manejo de Error Fatal: Si falla la creación, volvemos al selector
            console.error('[FATAL CRASH] Error al procesar la configuración y crear ventanas.', error.message, error.stack);
            logManager.logFatal('SELECTION_MADE_HANDLER', error); 
            
            windowManager.closeAllWindows();
            windowManager.createSelectorWindow();
        }
    });
}

module.exports = {
    registerHandlers
};