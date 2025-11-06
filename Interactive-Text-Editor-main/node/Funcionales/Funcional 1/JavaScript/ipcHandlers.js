// JavaScript/ipcHandlers.js

const { ipcMain, dialog, BrowserWindow } = require('electron');
const fs = require('fs');
const path = require('path');

// Modulos propios
const appState = require('./appState');
const pathManager = require('./pathManager'); // pathManager esta disponible en todo el archivo
const configManager = require('./configManager');
const windowManager = require('./windowManager');
const inactivityManager = require('./inactivityManager');
const { calculatePositions } = require('./positionCalculator');

function registerHandlers() {

    // ----------------------
    // Funcion para abrir el dialogo de seleccion de archivos
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
            defaultPath: pathManager.resourcesDir // <-- Se usa pathManager. directamente
        });

        if (result.canceled) {
            return null;
        }
        return result.filePaths;
    });

    // ----------------------
    // Crear todas las ventanas y cargar contenido
    // ----------------------
    ipcMain.on('selection-made', (e, { size, position, mediaFiles, distributionScheme, assignmentMap }) => {
        
        try {
            console.log('[SELECCION] Recibido:', { size, position, mediaFiles, distributionScheme, assignmentMap });
            
            windowManager.closeAllWindows();
            inactivityManager.clearInactivityTimer();

            const { mainBounds, otherBounds } = calculatePositions(size, parseInt(position));

            let finalOtherBounds = otherBounds;
            let userMediaMap = {};
            
            // --- LOGICA DE DISTRIBUCION AVANZADA ---
            if (size === '1') {
                const remainingBounds = otherBounds; 
                
                if (distributionScheme === 'one_big' && mediaFiles.length >= 1) {
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
                    finalOtherBounds = remainingBounds;
                    remainingBounds.forEach((bounds, idx) => {
                         userMediaMap[bounds.index] = mediaFiles[idx];
                         console.log(`[INDIVIDUAL] Asignado archivo ${idx} (${mediaFiles[idx]}) a index ${bounds.index}`);
                    });

                } else if (distributionScheme === 'none') {
                     finalOtherBounds = [];
                
                } else if (distributionScheme === 'two_halves' && mediaFiles.length >= 2) {
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
                // LOGICA PARA 1/2 PANTALLA
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

            // Cerrar selector
            if (appState.winSelector) {
                appState.winSelector.close();
                appState.winSelector = null;
            }

            // 1. Crear ventana principal
            const mainWin = windowManager.createWindow(mainBounds, true);
            appState.windows.push(mainWin);
            
            // 2. Crear ventanas de fondo
            const bgWindows = [];
            finalOtherBounds.forEach((bounds) => {
                const bgWin = windowManager.createWindow(bounds, false);
                appState.windows.push(bgWin);
                bgWindows.push(bgWin); // Guardar en una lista separada
            });
            
            // Guardar configuracion
            configManager.saveLastConfig({ 
                size, 
                position, 
                mediaFiles, 
                distributionScheme, 
                assignmentMap 
            });

            // ----------------------------------------------------
            // Al cargar la ventana principal (SOLO LOGICA DE MAINWIN)
            // ----------------------------------------------------
            mainWin.webContents.once('did-finish-load', () => {
                
                // --- CAMBIO CLAVE ---
                // Ya no destructuramos pathManager. Usaremos pathManager.propiedad
                
                const config = configManager.getConfig();
                
                const bannersTop = fs.existsSync(pathManager.bannersTopPath) 
                    ? fs.readdirSync(pathManager.bannersTopPath)
                        .filter(f => /\.\.(png|jpe?g|gif|webp)$/i.test(f) === false && /\.(png|jpe?g|gif|webp)$/i.test(f))
                        .map(f => pathManager.getFileUrl(path.join(pathManager.bannersTopPath,f))) // <-- CORREGIDO
                    : [];
                const bannersBottom = fs.existsSync(pathManager.bannersBottomPath) 
                    ? fs.readdirSync(pathManager.bannersBottomPath)
                        .filter(f => /\.(png|jpe?g|gif|webp)$/i.test(f))
                        .map(f => pathManager.getFileUrl(path.join(pathManager.bannersBottomPath,f))) // <-- CORREGIDO
                    : [];
                const mobileImgs = fs.existsSync(pathManager.mobileImgsPath) 
                    ? fs.readdirSync(pathManager.mobileImgsPath)
                        .filter(f => /\.(png|jpe?g|gif|webp)$/i.test(f))
                        .map(f => pathManager.getFileUrl(path.join(pathManager.mobileImgsPath,f))) // <-- CORREGIDO
                    : [];

                const watcher = fs.watch(pathManager.resourcesDir, (eventType, filename) => { // <-- CORREGIDO
                    if (filename === config.userFileName) { 
                        
                        inactivityManager.startInactivityTimer(mainWin); 

                        if (!fs.existsSync(pathManager.userFile)) { // <-- CORREGIDO
                            mainWin.webContents.send('no-file', { 
                                welcomePath: pathManager.getFileUrl(pathManager.welcomeImage) // <-- CORREGIDO
                            });
                        } else if (eventType === 'change') {
                            const text = fs.readFileSync(pathManager.userFile, 'utf-8'); // <-- CORREGIDO
                            mainWin.webContents.send('file-changed', text);
                            
                                // Al actualizar el archivo, respetamos la misma regla: solo enviar mobileImgs si es Pantalla completa
                                const mobileImgsToSendOnChange = (String(size) === '3') ? mobileImgs : [];
                                console.log('[MAIN] Enviando load-images por cambio. size=', size, 'mobileImgsToSendOnChange.length=', mobileImgsToSendOnChange.length);
                                mainWin.webContents.send('load-images', {
                                    bannersTop,
                                    bannersBottom,
                                    mobileImgs: mobileImgsToSendOnChange,
                                    mediaFiles: []
                                });
                        }
                    }
                });

                mainWin.on('closed', () => {
                    watcher.close();
                    inactivityManager.clearInactivityTimer();
                    windowManager.closeAllWindows(); // Cierra todas las demas ventanas (fondo)
                });

                // Carga inicial
                console.log(`[DIAGNOSTICO] Verificando archivo de usuario en: ${pathManager.userFile}`); // <-- CORREGIDO
                if (fs.existsSync(pathManager.userFile)) { // <-- CORREGIDO
                    console.log('[DIAGNOSTICO] Archivo encontrado. Cargando contenido.'); 
                    const text = fs.readFileSync(pathManager.userFile, 'utf-8'); // <-- CORREGIDO
                    mainWin.webContents.send('file-changed', text);
                    inactivityManager.startInactivityTimer(mainWin); 
                } else {
                    console.log(`[DIAGNOSTICO] Archivo NO encontrado. Cargando Bienvenida desde: ${pathManager.getFileUrl(pathManager.welcomeImage)}`); // <-- CORREGIDO
                    mainWin.webContents.send('no-file', { 
                        welcomePath: pathManager.getFileUrl(pathManager.welcomeImage) // <-- CORREGIDO
                    });
                }
                
                mainWin.webContents.send('window-size-selected', { size: size });

                // Solo enviamos las imagenes "moviles" cuando la configuracion es Pantalla completa (size === '3')
                const mobileImgsToSend = (String(size) === '3') ? mobileImgs : [];
                console.log('[MAIN] Enviando load-images inicial. size=', size, 'mobileImgsToSend.length=', mobileImgsToSend.length);

                mainWin.webContents.send('load-images', {
                    bannersTop,
                    bannersBottom,
                    mobileImgs: mobileImgsToSend,
                    mediaFiles: [] 
                });
            });


            // -----------------------------------------------------------
            // Al cargar las ventanas de fondo (LOGICA SEPARADA E INMEDIATA)
            // -----------------------------------------------------------
            console.log(`[DEBUG] Total de ventanas de fondo: ${bgWindows.length}`);
            
            bgWindows.forEach((bgWin, winIdx) => {
                console.log(`[DEBUG] Procesando ventana de fondo ${winIdx + 1}`);
                
                // Adjuntamos el listener INMEDIATAMENTE
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
                        
                        // --- ESTA ES LA LÍNEA DEL ERROR ---
                        // Corregida para usar pathManager.getFileUrl()
                        const mediaUrl = pathManager.getFileUrl(normalizedPath);
                        
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

        } catch (error) {
            console.error('[FATAL CRASH] Error al procesar la configuracion y crear ventanas.', error.message, error.stack);
            
            windowManager.closeAllWindows();
            windowManager.createSelectorWindow();
        }
    });
}

module.exports = {
    registerHandlers
};