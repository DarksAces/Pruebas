// JavaScript/ipcHandlers.js

const { ipcMain, dialog, BrowserWindow } = require('electron');
const fs = require('fs');
const path = require('path');

const appState = require('./appState');
const pathManager = require('./pathManager');
const configManager = require('./configManager');
const windowManager = require('./windowManager');
const inactivityManager = require('./inactivityManager');
const { calculatePositions } = require('./positionCalculator');

function sendTextToBackgrounds(eventName, data) {
    appState.backgroundWindows.forEach(bgWin => {
        if (!bgWin.isDestroyed()) {
            bgWin.webContents.send(eventName, data);
        }
    });
}

function handleSelectionMade(data) {
    const { size, position, mediaFiles, distributionScheme, assignmentMap } = data;
    
    try {
        console.log('[SELECCION] Recibido:', { size, position, mediaFiles, distributionScheme, assignmentMap });
        
        windowManager.closeAllWindows(); 
        inactivityManager.clearInactivityTimer();
        
        const { mainBounds } = calculatePositions(size, parseInt(position)); 
        
        // Obtenemos los datos de ambos monitores (APP Primary = Secundario Físico; APP Secondary = Principal Físico)
        const primaryDisplayData = windowManager.getPrimaryDisplay();
        const secondaryDisplayData = windowManager.getSecondaryDisplay();
        
        let bgWindows = []; 
        let userMediaMap = {}; 
        let finalOtherBounds = []; 

        if (secondaryDisplayData) {
            const { x: sx, y: sy, width: sw, height: sh } = secondaryDisplayData.bounds;
            const quarterPositionsSecondary = [
                { x: sx, y: sy, width: sw/2, height: sh/2, index: 1 },
                { x: sx + sw/2, y: sy, width: sw/2, height: sh/2, index: 2 },
                { x: sx, y: sy + sh/2, width: sw/2, height: sh/2, index: 3 },
                { x: sx + sw/2, y: sy + sh/2, width: sw/2, height: sh/2, index: 4 }
            ];
            
            if (size === '1') {
                const mainPositionIndex = parseInt(position);
                const remainingBounds = quarterPositionsSecondary.filter(b => b.index !== mainPositionIndex); 

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
                    remainingBounds.forEach((bounds, idx) => { userMediaMap[bounds.index] = mediaFiles[idx]; });
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
                    userMediaMap[98] = mediaFiles[assignmentMap.fusedFileIndex]; 
                    userMediaMap[individualBound.index] = mediaFiles[assignmentMap.individualFileIndex]; 
                }
            } else if (size === '2' && mediaFiles.length >= 1) {
                const halfPositionsSecondary = [
                     { x: sx, y: sy, width: sw/2, height: sh, index: 1 },
                     { x: sx + sw/2, y: sy, width: sw/2, height: sh, index: 2 },
                     { x: sx, y: sy, width: sw, height: sh/2, index: 3 },
                     { x: sx, y: sy + sh/2, width: sw, height: sh/2, index: 4 }
                ];
                let otherIndex;
                const mainPositionIndex = parseInt(position);
                if (mainPositionIndex === 1) otherIndex = 2; 
                else if (mainPositionIndex === 2) otherIndex = 1; 
                else if (mainPositionIndex === 3) otherIndex = 4; 
                else if (mainPositionIndex === 4) otherIndex = 3; 
                if (otherIndex) {
                    const otherPos = halfPositionsSecondary[otherIndex - 1];
                    finalOtherBounds = [otherPos];
                    userMediaMap[otherPos.index] = mediaFiles[0];
                }
            } else if (size === '3') {
                finalOtherBounds = [{ x: sx, y: sy, width: sw, height: sh, index: 100, isFullScreen: true }];
                if (mediaFiles.length >= 1) {
                    userMediaMap[100] = mediaFiles[0];
                }
            }
        }
        
        if (appState.winSelector) { appState.winSelector.close(); appState.winSelector = null; }

        const mainWin = windowManager.createWindow(mainBounds, true, pathManager.indexHtml);
        
        if (secondaryDisplayData) { 
            finalOtherBounds.forEach((bounds) => {
                const bgWin = windowManager.createWindow(bounds, false, pathManager.backgroundHtml);
                bgWindows.push(bgWin); 
            });
        }
        
        configManager.saveLastConfig({ size, position, mediaFiles, distributionScheme, assignmentMap });

        let initialText = null;
        let fileExists = fs.existsSync(pathManager.userFile);
        if (fileExists) { initialText = fs.readFileSync(pathManager.userFile, 'utf-8'); }

        // ----------------------------------------------------
        // Al cargar la ventana principal (index.html)
        // ----------------------------------------------------
        mainWin.webContents.once('did-finish-load', () => {
            
            const config = configManager.getConfig();
            
            const bannersTop = fs.existsSync(pathManager.bannersTopPath) 
                ? fs.readdirSync(pathManager.bannersTopPath)
                    .filter(f => /\.(png|jpe?g|gif|webp)$/i.test(f))
                    .map(f => pathManager.getFileUrl(path.join(pathManager.bannersTopPath,f))) : [];
            const bannersBottom = fs.existsSync(pathManager.bannersBottomPath) 
                ? fs.readdirSync(pathManager.bannersBottomPath)
                    .filter(f => /\.(png|jpe?g|gif|webp)$/i.test(f))
                    .map(f => pathManager.getFileUrl(path.join(pathManager.bannersBottomPath,f))) : [];
            const mobileImgs = fs.existsSync(pathManager.mobileImgsPath) 
                ? fs.readdirSync(pathManager.mobileImgsPath)
                    .filter(f => /\.(png|jpe?g|gif|webp|mp4|webm|ogg|mov|avi)$/i.test(f))
                    .map(f => pathManager.getFileUrl(path.join(pathManager.mobileImgsPath,f))) : [];

            const watcher = fs.watch(pathManager.resourcesDir, (eventType, filename) => {
                if (filename === config.userFileName) { 
                    
                    inactivityManager.startInactivityTimer(mainWin); 

                    if (!fs.existsSync(pathManager.userFile)) {
                        mainWin.webContents.send('no-file', { welcomePath: pathManager.getFileUrl(pathManager.welcomeImage) });
                        if (appState.backgroundWindows.length > 0) { sendTextToBackgrounds('background-no-file'); }
                    } else if (eventType === 'change') {
                        const text = fs.readFileSync(pathManager.userFile, 'utf-8');
                        
                        mainWin.webContents.send('file-changed', text);
                        
                        if (appState.backgroundWindows.length > 0) { sendTextToBackgrounds('background-text-changed', text); }
                        
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
                windowManager.closeAllWindows(); 
            });

            // Carga inicial (PRINCIPAL)
            if (fileExists) {
                mainWin.webContents.send('file-changed', initialText);
                inactivityManager.startInactivityTimer(mainWin); 
            } else {
                mainWin.webContents.send('no-file', { welcomePath: pathManager.getFileUrl(pathManager.welcomeImage) });
            }
            
            // Envío de window-size-selected y load-images inicial (PRINCIPAL)
            mainWin.webContents.send('window-size-selected', { size: size });
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
        // Al cargar las ventanas de fondo (background.html) - Sincronización robusta
        // -----------------------------------------------------------
        console.log(`[DEBUG] Total de ventanas de fondo: ${bgWindows.length}`);
        
        bgWindows.forEach((bgWin, winIdx) => {
            bgWin.webContents.once('did-finish-load', () => {
                const positionIndex = bgWin.positionIndex;
                const mediaFilePath = userMediaMap[positionIndex];
                
                // 1. Envío de MEDIA (inmediato)
                if (mediaFilePath) {
                    const fileName = path.basename(mediaFilePath);
                    const isVideo = /\.(mp4|webm|ogg|mov|avi)$/i.test(fileName); 
                    const isGif = /\.(gif)$/i.test(fileName);
                    const normalizedPath = path.normalize(mediaFilePath);
                    const mediaUrl = pathManager.getFileUrl(normalizedPath);
                    const mediaForWindow = {
                        type: isVideo ? 'video' : isGif ? 'gif' : 'image',
                        src: mediaUrl,
                        name: fileName,
                        priority: positionIndex
                    };

                    console.log(`[ENVIANDO MEDIA] A ventana index ${positionIndex}:`, mediaForWindow);

                    bgWin.webContents.send('load-images', { mediaFiles: [mediaForWindow] });
                } else {
                    console.log(`[VENTANA FONDO] Index ${positionIndex} - Sin archivo asignado.`);
                }

                // 2. Sincronización de TEXTO con retraso explícito
                setTimeout(() => {
                    if (fileExists) {
                        console.log(`[SINCRONIZACION TIMEOUT] Enviando texto inicial a fondo index ${positionIndex}.`);
                        bgWin.webContents.send('background-text-changed', initialText);
                    } else {
                        console.log(`[SINCRONIZACION TIMEOUT] Enviando no-file a fondo index ${positionIndex}.`);
                        bgWin.webContents.send('background-no-file');
                    }
                }, 50); 
            });
        });

    } catch (error) {
        console.error('[FATAL CRASH] Error al procesar la configuracion y crear ventanas.', error.message, error.stack);
        windowManager.closeAllWindows();
        windowManager.createSelectorWindow();
    }
}


function registerHandlers() {
    ipcMain.handle('open-media-dialog', async (event, maxFiles) => {
        const window = BrowserWindow.fromWebContents(event.sender);
        const properties = ['openFile'];
        if (maxFiles > 1) { properties.push('multiSelections'); }

        const result = await dialog.showOpenDialog(window, {
            properties: properties,
            filters: [ { name: 'Media', extensions: ['png', 'jpg', 'jpeg', 'gif', 'webp', 'mp4'] } ],
            message: `Selecciona hasta ${maxFiles} archivos de imagen o video.`,
            defaultPath: pathManager.resourcesDir
        });

        if (result.canceled) { return null; }
        return result.filePaths;
    });

    ipcMain.on('selection-made', (e, data) => handleSelectionMade(data));
}

module.exports = {
    registerHandlers,
    handleSelectionMade 
};