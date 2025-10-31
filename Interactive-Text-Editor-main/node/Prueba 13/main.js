// main.js

const { app, BrowserWindow, ipcMain, screen, dialog } = require('electron');
const path = require('path');
const fs = require('fs');
const url = require('url'); 

let winSelector;
let windows = [];
const LAST_CONFIG_KEY = 'lastConfiguration';

// ----------------------
// GESTIÓN DE CONFIGURACIÓN
// ----------------------
const configPath = path.join(__dirname, 'config.json');
let config;

try {
    const configData = fs.readFileSync(configPath, 'utf-8');
    config = JSON.parse(configData);
    console.log('[CONFIG] Archivo de configuración cargado con éxito.');
} catch (error) {
    console.error('[CONFIG FATAL ERROR] No se pudo cargar o parsear config.json. ¡La aplicación no puede continuar!', error);
    app.quit(); 
}

function saveLastConfig(data) {
    try {
        const currentConfigData = fs.readFileSync(configPath, 'utf-8');
        let currentConfig = JSON.parse(currentConfigData);
        currentConfig[LAST_CONFIG_KEY] = data;
        fs.writeFileSync(configPath, JSON.stringify(currentConfig, null, 2), 'utf-8');
        console.log('[CONFIG] Ultima configuración guardada con exito.');
    } catch (error) {
        console.error('[CONFIG ERROR] No se pudo guardar la ultima configuración:', error);
    }
}

function loadLastConfig() {
    if (config && config[LAST_CONFIG_KEY]) {
        console.log('[INIT] Ultima configuración encontrada.');
        return config[LAST_CONFIG_KEY];
    }
    return null;
}

// ----------------------
// GESTIÓN DE INACTIVIDAD
// ----------------------
let inactivityTimer = null;
const INACTIVITY_TIME_MS = config.inactivityTimeMs; 

// ----------------------
// Directorios Absolutos
// ----------------------
const resourcesDir = path.resolve(config.resourcesDir); 
console.log(`[DIAGNOSTICO] Ruta de recursos resuelta: ${resourcesDir}`);
const htmlDir = path.join(__dirname, config.htmlDirName); 
const imagesDir = path.join(resourcesDir, config.imageDirName); 
const userFile = path.join(resourcesDir, config.userFileName); 
const welcomeImage = path.join(imagesDir, config.defaultWelcomeImagePath); 

// ----------------------
// Ventana selector
// ----------------------
function createSelectorWindow() {
    if (winSelector) return;
    
    winSelector = new BrowserWindow({
        width: 450, 
        height: 650,
        frame: true,
        resizable: false,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
            contextIsolation: true,
            nodeIntegration: false
        }
    });
    winSelector.loadFile(path.join(htmlDir, 'selector.html'));

    winSelector.on('closed', () => {
        if (!windows.length) {
            app.quit();
        }
    });
}

// ----------------------
// Crear ventana
// ----------------------
function createWindow(bounds, isMain = false) {
    console.log(`[VENTANA] Creando ventana ${isMain ? 'PRINCIPAL' : 'FONDO'} en:`, bounds);
    
    const isTransparent = !isMain; 

    const win = new BrowserWindow({
        x: bounds.x,
        y: bounds.y,
        width: bounds.width,
        height: bounds.height,
        frame: false,
        transparent: isTransparent, 
        resizable: false,
        alwaysOnTop: true, 
        focusable: isMain, 
        skipTaskbar: !isMain, 
        backgroundColor: '#000000',
        hasShadow: false,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
            contextIsolation: true,
            webSecurity: false 
        }
    });

    win.setAlwaysOnTop(true, 'screen-saver');
    
    if (isMain) {
        win.loadFile(path.join(htmlDir, 'index.html'));
        win.setIgnoreMouseEvents(false);
        
        // Registrar atajo de teclado para volver al selector
        win.webContents.on('before-input-event', (event, input) => {
            if (input.control && input.shift && input.key.toLowerCase() === 'r') {
                console.log('[ATAJO] Ctrl+Shift+R detectado - Volviendo al selector');
                event.preventDefault();
                
                // Cerrar todas las ventanas
                windows.forEach(w => {
                    if (!w.isDestroyed()) {
                        w.close();
                    }
                });
                windows = [];
                
                // Limpiar temporizador
                if (inactivityTimer) {
                    clearTimeout(inactivityTimer);
                    inactivityTimer = null;
                }
                
                // Abrir selector
                createSelectorWindow();
            }
        });
    } else {
        win.loadFile(path.join(htmlDir, 'background.html'));
        win.setIgnoreMouseEvents(true);
    }
    
    if (bounds.index !== undefined) {
        win.positionIndex = bounds.index;
    }

    return win;
}

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
        defaultPath: resourcesDir 
    });

    if (result.canceled) {
        return null;
    }
    return result.filePaths;
});

// ----------------------
// LÓGICA DEL TEMPORIZADOR Y RESET
// ----------------------
function resetToWelcome(mainWin) {
    if (fs.existsSync(userFile)) {
        fs.unlink(userFile, (err) => { 
            if (err) {
                console.error('Error al eliminar contenido.txt por inactividad:', err);
            } else {
                console.log('contenido.txt eliminado por inactividad. Volviendo a bienvenida.');
            }
            if (mainWin && !mainWin.isDestroyed()) {
                 mainWin.webContents.send('no-file', {
                     welcomePath: url.pathToFileURL(welcomeImage).href
                 });
            }
        });
    } else {
        if (mainWin && !mainWin.isDestroyed()) {
            mainWin.webContents.send('no-file', {
                welcomePath: url.pathToFileURL(welcomeImage).href
            });
        }
    }
}

function startInactivityTimer(mainWin) {
    if (inactivityTimer) {
        clearTimeout(inactivityTimer);
    }
    inactivityTimer = setTimeout(() => {
        resetToWelcome(mainWin);
    }, INACTIVITY_TIME_MS);
    console.log(`[TEMPORIZADOR] Reiniciado. El archivo se eliminara en ${INACTIVITY_TIME_MS / 1000} segundos si no hay cambios.`);
}

// ----------------------
// CÁLCULO DE POSICIONES (Superposición de Ventana Principal)
// ----------------------

function calculatePositions(size, selectedPos) {
    const displays = screen.getAllDisplays();
    const targetDisplay = displays.length > 1 ? displays[1] : displays[0];

    const { width: sw, height: sh, x: sx, y: sy } = targetDisplay.bounds;

    console.log(`[DIAGNOSTICO] Display Target - X:${sx}, Y:${sy}, W:${sw}, H:${sh}`);

    const quarterPositionsBase = [
        { x: sx, y: sy, width: sw/2, height: sh/2, index: 1 },
        { x: sx + sw/2, y: sy, width: sw/2, height: sh/2, index: 2 },
        { x: sx, y: sy + sh/2, width: sw/2, height: sh/2, index: 3 },
        { x: sx + sw/2, y: sy + sh/2, width: sw/2, height: sh/2, index: 4 }
    ];
    
    if (size === "3") {
        return {
            mainBounds: { x: sx, y: sy, width: sw, height: sh, index: 0 }, 
            otherBounds: []
        };
    }
    
    if (size === "2") {
        const halfPositions = [
             { x: sx, y: sy, width: sw/2, height: sh, index: 1 },
             { x: sx + sw/2, y: sy, width: sw/2, height: sh, index: 2 },
             { x: sx, y: sy, width: sw, height: sh/2, index: 3 },
             { x: sx, y: sy + sh/2, width: sw, height: sh/2, index: 4 }
        ];

        const mainPos = halfPositions[selectedPos - 1];
        
        let otherIndex;
        if (selectedPos === 1) otherIndex = 2; 
        else if (selectedPos === 2) otherIndex = 1; 
        else if (selectedPos === 3) otherIndex = 4; 
        else if (selectedPos === 4) otherIndex = 3; 
        
        const otherPos = halfPositions[otherIndex - 1];

        return { mainBounds: mainPos, otherBounds: [otherPos] };
    }
    
    if (size === "1") {
        const mainPosBase = quarterPositionsBase[selectedPos - 1];
        const pixelAdj = 1;

        let mainBounds = { ...mainPosBase };
        
        if (selectedPos === 1 || selectedPos === 3) {
            mainBounds.width += pixelAdj; 
        }
        if (selectedPos === 1 || selectedPos === 2) {
            mainBounds.height += pixelAdj;
        }
        if (selectedPos === 2 || selectedPos === 4) {
            mainBounds.x -= pixelAdj;
            mainBounds.width += pixelAdj;
        }
        if (selectedPos === 3 || selectedPos === 4) {
            mainBounds.y -= pixelAdj;
            mainBounds.height += pixelAdj;
        }

        const others = quarterPositionsBase
            .filter(pos => pos.index !== selectedPos)
            .map(pos => pos);

        return { mainBounds: mainBounds, otherBounds: others };
    }
}

// ----------------------
// Crear todas las ventanas y cargar contenido
// ----------------------
ipcMain.on('selection-made', (e, { size, position, mediaFiles, distributionScheme, assignmentMap }) => {
    
    try {
        console.log('[SELECCION] Recibido:', { size, position, mediaFiles, distributionScheme, assignmentMap });
        
        windows.forEach(w => w.close());
        windows = [];
        
        if (inactivityTimer) {
            clearTimeout(inactivityTimer);
            inactivityTimer = null;
        }

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

                console.log('[FUSIONADO] Fondo unico creado:', combinedBounds);
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
            // LÓGICA PARA 1/2 PANTALLA
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
        if (winSelector) {
            winSelector.close();
            winSelector = null;
        }

        // 1. Crear ventana principal
        const mainWin = createWindow(mainBounds, true);
        windows.push(mainWin);
        
        // 2. Crear ventanas de fondo
        finalOtherBounds.forEach((bounds) => {
            const bgWin = createWindow(bounds, false);
            windows.push(bgWin);
        });
        
        // Guardar configuración
        saveLastConfig({ 
            size, 
            position, 
            mediaFiles, 
            distributionScheme, 
            assignmentMap 
        });

        // ----------------------
        // Al cargar la ventana principal 
        // ----------------------
        mainWin.webContents.once('did-finish-load', () => {
            
            const bannersTopPath = path.join(imagesDir, config.bannersTopDirName); 
            const bannersBottomPath = path.join(imagesDir, config.bannersBottomDirName); 
            const mobileImgsPath = path.join(imagesDir, config.mobileImgsDirName); 

            const bannersTop = fs.existsSync(bannersTopPath) 
                ? fs.readdirSync(bannersTopPath)
                    .filter(f => /\.(png|jpe?g|gif|webp)$/i.test(f))
                    .map(f => url.pathToFileURL(path.join(bannersTopPath,f)).href) 
                : [];
            const bannersBottom = fs.existsSync(bannersBottomPath) 
                ? fs.readdirSync(bannersBottomPath)
                    .filter(f => /\.(png|jpe?g|gif|webp)$/i.test(f))
                    .map(f => url.pathToFileURL(path.join(bannersBottomPath,f)).href) 
                : [];
            const mobileImgs = fs.existsSync(mobileImgsPath) 
                ? fs.readdirSync(mobileImgsPath)
                    .filter(f => /\.(png|jpe?g|gif|webp)$/i.test(f))
                    .map(f => url.pathToFileURL(path.join(mobileImgsPath,f)).href) 
                : [];

            const watcher = fs.watch(resourcesDir, (eventType, filename) => {
                if (filename === config.userFileName) { 
                    
                    startInactivityTimer(mainWin); 

                    if (!fs.existsSync(userFile)) {
                        mainWin.webContents.send('no-file', { 
                            welcomePath: url.pathToFileURL(welcomeImage).href 
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
                if (inactivityTimer) {
                    clearTimeout(inactivityTimer);
                    inactivityTimer = null;
                }
                
                windows.forEach(w => {
                    if (!w.isDestroyed()) {
                        w.close();
                    }
                });
                windows = [];
            });

            // Carga inicial
            console.log(`[DIAGNOSTICO] Verificando archivo de usuario en: ${userFile}`); 
            if (fs.existsSync(userFile)) {
                console.log('[DIAGNOSTICO] Archivo encontrado. Cargando contenido.'); 
                const text = fs.readFileSync(userFile, 'utf-8');
                mainWin.webContents.send('file-changed', text);
                startInactivityTimer(mainWin); 
            } else {
                console.log(`[DIAGNOSTICO] Archivo NO encontrado. Cargando Bienvenida desde: ${url.pathToFileURL(welcomeImage).href}`);
                mainWin.webContents.send('no-file', { 
                    welcomePath: url.pathToFileURL(welcomeImage).href 
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
            const bgWindows = windows.filter(w => w !== mainWin);
            
            console.log(`[DEBUG] Total de ventanas de fondo: ${bgWindows.length}`);
            
            bgWindows.forEach((bgWin, winIdx) => {
                console.log(`[DEBUG] Procesando ventana de fondo ${winIdx + 1}`);
                
                bgWin.webContents.once('did-finish-load', () => {
                    const positionIndex = bgWin.positionIndex;
                    const mediaFilePath = userMediaMap[positionIndex];
                    
                    console.log(`[VENTANA FONDO] Index ${positionIndex} - Archivo: ${mediaFilePath}`);
                    
                    if (mediaFilePath) {
                        // Verificar que el archivo existe
                        if (!fs.existsSync(mediaFilePath)) {
                            console.error(`[ERROR] El archivo NO existe: ${mediaFilePath}`);
                            return;
                        }
                        
                        console.log(`[OK] El archivo existe: ${mediaFilePath}`);
                        
                        const fileName = path.basename(mediaFilePath);
                        const isVideo = /\.(mp4)$/i.test(fileName);
                        const isGif = /\.(gif)$/i.test(fileName);
                        
                        // Normalizar la ruta
                        const normalizedPath = path.normalize(mediaFilePath);
                        const mediaUrl = url.pathToFileURL(normalizedPath).href;
                        
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
        console.error('[FATAL CRASH] Error al procesar la configuración y crear ventanas.', error.message, error.stack);
        
        windows.forEach(w => {
            if (!w.isDestroyed()) {
                w.close();
            }
        });
        windows = [];
        
        createSelectorWindow();
    }
});

// ----------------------
// App ready
// ----------------------
app.whenReady().then(() => {
    const lastConfig = loadLastConfig();
    
    if (lastConfig && lastConfig.size) {
        process.nextTick(() => {
            ipcMain.emit('selection-made', null, lastConfig); 
        });
    } else {
        createSelectorWindow();
    }
});

// ----------------------
// Cerrar app
// ----------------------
app.on('window-all-closed', () => { 
    if (process.platform !== 'darwin') app.quit(); 
});