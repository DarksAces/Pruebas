// JavaScript/ipcHandlers.js (FINAL Y FUNCIONAL)

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

// ----------------------------------------------------
// HELPER MOVIDO AL ÁMBITO SUPERIOR (Para ser accesible)
// ----------------------------------------------------
const getMediaUrls = (dirPath) => {
    if (fs.existsSync(dirPath)) {
        return fs.readdirSync(dirPath)
            .filter(f => /\.(png|jpe?g|gif|webp|mp4)$/i.test(f))
            .map(f => pathManager.getFileUrl(path.join(dirPath, f)));
    }
    return [];
};

function registerHandlers() {

    // ----------------------
    // HANDLER 1: Diálogo de Selección de Archivos
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
    // HANDLER 2: Procesar Selección (CORE LOGIC)
    // ----------------------
    ipcMain.on('selection-made', (e, selectionData) => {
        const { size, position, mediaFiles, distributionScheme, assignmentMap } = selectionData;
        
        try {
            logManager.log('INFO', 'SELECTION_RECEIVED', `Nueva selección: Tamaño=${size}, Posición=${position}, Archivos=${mediaFiles.length}`); 
            configManager.saveLastConfig(selectionData);
            
            windowManager.closeAllWindows();
            inactivityManager.clearInactivityTimer();

            const { mainBounds, otherBounds } = calculatePositions(size, parseInt(position));

            let finalOtherBounds = otherBounds;
            let userMediaMap = {};
            
            // --- CÁLCULO DE RUTAS DE BANNERS Y CREACIÓN DE DIRECTORIOS ---
            const config = configManager.getConfig(); 
            
            // 1. Crear carpeta de recursos relativa (media_content) si no existe
            if (!fs.existsSync(pathManager.resourcesDir)) {
                fs.mkdirSync(pathManager.resourcesDir, { recursive: true });
                logManager.log('INFO', 'RESOURCES_DIR_CREATED', `Carpeta de recursos creada: ${pathManager.resourcesDir}`);
            }

            // 2. Definir las variables multimedia (ACCESIBLES en el Watcher)
            const bannersTop = getMediaUrls(pathManager.bannersTopPath);
            const bannersBottom = getMediaUrls(pathManager.bannersBottomPath);
            const mobileImgs = getMediaUrls(pathManager.mobileImgsPath);
            // ----------------------------------------------------

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
                if (otherBounds.length > 0) {
                    finalOtherBounds = otherBounds;
                    userMediaMap[otherBounds[0].index] = mediaFiles[0];
                }
            } else if (size === '3') {
                finalOtherBounds = [];
            }
            // ... (FIN LÓGICA DE DISTRIBUCIÓN AVANZADA)

            if (appState.winSelector) { appState.winSelector.close(); appState.winSelector = null; }

            const mainWin = windowManager.createWindow(mainBounds, true);
            appState.windows.push(mainWin);
            
            const bgWindows = [];
            finalOtherBounds.forEach((bounds) => {
                const bgWin = windowManager.createWindow(bounds, false);
                appState.windows.push(bgWin);
                bgWindows.push(bgWin); 
            });
            
            logManager.log('INFO', 'WINDOWS_CREATED', `Ventanas principal y ${finalOtherBounds.length} de fondo creadas con éxito.`); 
            
            // ----------------------------------------------------
            // GESTIÓN DE LA VENTANA PRINCIPAL (Carga de assets)
            // ----------------------------------------------------
            mainWin.webContents.once('did-finish-load', () => {
                
                // --- RUTAS PARA EL WATCHER (CORRECCIÓN DE RUTA ABSOLUTA) ---
                const fileToWatchPath = pathManager.userFile; // Ej: c:\estacio\display.txt
                const directoryToWatch = path.dirname(fileToWatchPath); // Ej: c:\estacio
                const filenameToWatch = path.basename(fileToWatchPath); // Ej: display.txt

                // Crear directorio de contenido de usuario (c:\estacio) si no existe
                if (!fs.existsSync(directoryToWatch)) {
                    fs.mkdirSync(directoryToWatch, { recursive: true });
                    logManager.log('INFO', 'USER_CONTENT_DIR_CREATED', `Carpeta de contenido de usuario creada: ${directoryToWatch}`);
                }
                
                // WATCHER: Vigila cambios en el archivo de contenido
                const watcher = fs.watch(directoryToWatch, (eventType, filename) => { 
                    if (filename === filenameToWatch) { 
                        
                        inactivityManager.startInactivityTimer(mainWin); 

                        if (!fs.existsSync(fileToWatchPath)) { 
                            mainWin.webContents.send('no-file', {});
                        } else if (eventType === 'change') {
                            const text = fs.readFileSync(fileToWatchPath, 'utf-8'); 
                            mainWin.webContents.send('file-changed', text);
                            
                            // Recargar imágenes
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
                if (fs.existsSync(fileToWatchPath)) { 
                    const text = fs.readFileSync(fileToWatchPath, 'utf-8'); 
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
            // Manejo de Error Fatal
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