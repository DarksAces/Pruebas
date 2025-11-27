// JavaScript/ipcHandlers.js (CORREGIDO + LOGGING)

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
const logManager = require('./logManager'); // <-- ¡IMPORTADO!

function registerHandlers() {

    // ----------------------
    // Función para abrir el diálogo de selección de archivos
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
    // Crear todas las ventanas y cargar contenido
    // ----------------------
    ipcMain.on('selection-made', (e, { size, position, mediaFiles, distributionScheme, assignmentMap }) => {
        
        try {
            logManager.log('INFO', 'SELECTION_RECEIVED', `Nueva selección: Tamaño=${size}, Posición=${position}, Archivos=${mediaFiles.length}`); 
            console.log('[SELECCION] Recibido:', { size, position, mediaFiles, distributionScheme, assignmentMap });
            
            windowManager.closeAllWindows();
            inactivityManager.clearInactivityTimer();

            const { mainBounds, otherBounds } = calculatePositions(size, parseInt(position));

            let finalOtherBounds = otherBounds;
            let userMediaMap = {};
            
            // --- LÓGICA DE DISTRIBUCIÓN AVANZADA ---
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

                } else if (distributionScheme === 'three_individual' && mediaFiles.length >= 3) {
                    finalOtherBounds = remainingBounds;
                    remainingBounds.forEach((bounds, idx) => {
                         userMediaMap[bounds.index] = mediaFiles[idx];
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
                }
            } else if (size === '2' && mediaFiles.length >= 1) {
                // LÓGICA PARA 1/2 PANTALLA
                if (otherBounds.length > 0) {
                    finalOtherBounds = otherBounds;
                    userMediaMap[otherBounds[0].index] = mediaFiles[0];
                }
            } else if (size === '3') {
                // Pantalla completa no tiene fondos
                finalOtherBounds = [];
            }


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
                bgWindows.push(bgWin); 
            });
            
            // Guardar configuración
            configManager.saveLastConfig({ 
                size, 
                position, 
                mediaFiles, 
                distributionScheme, 
                assignmentMap 
            });

            // LOG INFORMATIVO DE CREACIÓN DE VENTANAS (DESPUÉS DE LA CREACIÓN)
            logManager.log('INFO', 'WINDOWS_CREATED', `Ventanas principal y ${finalOtherBounds.length} de fondo creadas con éxito.`); 
            
            // ----------------------------------------------------
            // Al cargar la ventana principal (SOLO LÓGICA DE MAINWIN)
            // ----------------------------------------------------
            mainWin.webContents.once('did-finish-load', () => {
                
                const config = configManager.getConfig();
                
                // Función auxiliar para leer y mapear archivos de imagen/video a URLs
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

                const watcher = fs.watch(pathManager.resourcesDir, (eventType, filename) => { 
                    if (filename === config.userFileName) { 
                        
                        inactivityManager.startInactivityTimer(mainWin); 

                        if (!fs.existsSync(pathManager.userFile)) { 
                            // ******************************************************
                            // CORRECCIÓN: Se envía un objeto vacío, eliminando welcomePath
                            mainWin.webContents.send('no-file', {});
                            // ******************************************************
                        } else if (eventType === 'change') {
                            const text = fs.readFileSync(pathManager.userFile, 'utf-8'); 
                            mainWin.webContents.send('file-changed', text);
                            
                            // Reenviar banners/móviles para refrescar la carga si es necesario
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
                    windowManager.closeAllWindows(); 
                });

                // Carga inicial
                if (fs.existsSync(pathManager.userFile)) { 
                    const text = fs.readFileSync(pathManager.userFile, 'utf-8'); 
                    mainWin.webContents.send('file-changed', text);
                    inactivityManager.startInactivityTimer(mainWin); 
                } else {
                    // ******************************************************
                    // CORRECCIÓN: Se envía un objeto vacío, eliminando welcomePath
                    mainWin.webContents.send('no-file', {}); 
                    // ******************************************************
                }
                
                mainWin.webContents.send('window-size-selected', { size: size });
                
                mainWin.webContents.send('load-images', {
                    bannersTop,
                    bannersBottom,
                    mobileImgs,
                    mediaFiles: [] 
                });
            });


            // -----------------------------------------------------------
            // Al cargar las ventanas de fondo 
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
                        
                        // CORRECCIÓN CLAVE: Usar pathManager.getFileUrl() para rutas de archivo locales
                        const mediaUrl = pathManager.getFileUrl(normalizedPath);
                        
                        const mediaForWindow = {
                            type: isVideo ? 'video' : isGif ? 'gif' : 'image',
                            src: mediaUrl,
                            name: fileName,
                            priority: positionIndex
                        };

                        bgWin.webContents.send('load-images', {
                            mediaFiles: [mediaForWindow]
                        });
                    } else {
                         // Manejar caso sin archivo asignado o archivo no encontrado (el background.html ya maneja el error de carga)
                         console.log(`[VENTANA FONDO] Index ${positionIndex} - Sin archivo asignado o archivo no encontrado.`);
                         bgWin.webContents.send('load-images', { mediaFiles: [] });
                    }
                });
            });

        } catch (error) {
            console.error('[FATAL CRASH] Error al procesar la configuración y crear ventanas.', error.message, error.stack);
            logManager.logFatal('SELECTION_MADE_HANDLER', error); // <-- ¡LOGGING AÑADIDO!
            
            windowManager.closeAllWindows();
            windowManager.createSelectorWindow();
        }
    });
}

module.exports = {
    registerHandlers
};