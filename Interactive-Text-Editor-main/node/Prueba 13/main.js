// main.js

const { app, BrowserWindow, ipcMain, screen, dialog } = require('electron');
const path = require('path');
const fs = require('fs');
const url = require('url'); 

let winSelector;
let windows = [];
const LAST_CONFIG_KEY = 'lastConfiguration'; // Clave para guardar en config.json

// ----------------------
// 1. GESTIÓN DE CONFIGURACIÓN
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

// Función para guardar la última configuración usada
function saveLastConfig(data) {
    try {
        const currentConfigData = fs.readFileSync(configPath, 'utf-8');
        let currentConfig = JSON.parse(currentConfigData);

        // Almacena solo los parámetros esenciales de la selección
        currentConfig[LAST_CONFIG_KEY] = data;

        fs.writeFileSync(configPath, JSON.stringify(currentConfig, null, 2), 'utf-8');
        console.log('[CONFIG] Última configuración guardada con éxito.');
    } catch (error) {
        console.error('[CONFIG ERROR] No se pudo guardar la última configuración:', error);
    }
}

// Función para cargar la última configuración guardada
function loadLastConfig() {
    if (config && config[LAST_CONFIG_KEY]) {
        console.log('[INIT] Última configuración encontrada.');
        return config[LAST_CONFIG_KEY];
    }
    return null;
}
// ----------------------


// ----------------------
// GESTIÓN DE INACTIVIDAD
// ----------------------
let inactivityTimer = null;
const INACTIVITY_TIME_MS = config.inactivityTimeMs; 

// ----------------------
// Directorios Absolutos
// ----------------------
const resourcesDir = path.resolve(config.resourcesDir); 
console.log(`[DIAGNÓSTICO] Ruta de recursos resuelta: ${resourcesDir}`);
const htmlDir = path.join(__dirname, config.htmlDirName); 
const imagesDir = path.join(resourcesDir, config.imageDirName); 
const userFile = path.join(resourcesDir, config.userFileName); 
const welcomeImage = path.join(imagesDir, config.defaultWelcomeImagePath); 
// ----------------------

// ----------------------
// Ventana selector
// ----------------------
function createSelectorWindow() {
    if (winSelector) return;
    
    winSelector = new BrowserWindow({
        width: 450, 
        height: 650, // Aumentado para la nueva UI
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
        // Cierra la app si no hay ventanas de contenido abiertas (solo si se cierra el selector manualmente)
        if (!windows.length) {
            app.quit();
        }
    });
}

// ----------------------
// Crear ventana (webSecurity: false asegurado)
// ----------------------
function createWindow(bounds, isMain = false) {
    const win = new BrowserWindow({
        x: bounds.x,
        y: bounds.y,
        width: bounds.width,
        height: bounds.height,
        frame: false,
        transparent: true,
        resizable: false,
        alwaysOnTop: true, 
        focusable: false,
        backgroundColor: '#00000000',
        hasShadow: false,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
            contextIsolation: true,
            // CLAVE: Permite cargar archivos locales (file://) sin restricción
            webSecurity: false 
        }
    });

    win.setAlwaysOnTop(true, 'normal'); 
    win.moveTop();

    if (isMain) {
        win.loadFile(path.join(htmlDir, 'index.html'));
        win.setIgnoreMouseEvents(false);
    } else {
        win.loadFile(path.join(htmlDir, 'background.html'));
        win.setIgnoreMouseEvents(true); 
    }
    
    if (bounds.index) {
        win.positionIndex = bounds.index;
    }

    return win;
}

// ----------------------
// Función para abrir el diálogo de selección de archivos (sin cambios)
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
// LÓGICA DEL TEMPORIZADOR Y RESET (sin cambios)
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


// Update calculatePositions para retornar el índice de posición absoluta (1-4)
function calculatePositions(size, selectedPos) {
    const displays = screen.getAllDisplays();
    const targetDisplay = displays.length > 1 ? displays[1] : displays[0];

    // Usamos bounds para superponer la barra de tareas
    const { width: sw, height: sh, x: sx, y: sy } = targetDisplay.bounds;

    console.log(`[DIAGNÓSTICO] Área Total (Bounds) - X:${sx}, Y:${sy}, W:${sw}, H:${sh}`);

    const quarterPositions = [
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
        const mainPos = quarterPositions[selectedPos - 1];
        
        const others = quarterPositions
            .filter(pos => pos.index !== selectedPos)
            .map(pos => pos); 

        return { mainBounds: mainPos, otherBounds: others };
    }
}


// ----------------------
// Crear todas las ventanas y cargar contenido
// ----------------------
// AHORA RECIBE EL distributionScheme y assignmentMap
ipcMain.on('selection-made', (e, { size, position, mediaFiles, distributionScheme, assignmentMap }) => {
    
    console.log('Recibido:', { size, position, mediaFiles, distributionScheme, assignmentMap });
    
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
            // Caso 1: FUSIONAR LAS 3
            const minX = Math.min(...remainingBounds.map(b => b.x));
            const minY = Math.min(...remainingBounds.map(b => b.y));
            const maxX = Math.max(...remainingBounds.map(b => b.x + b.width));
            const maxY = Math.max(...remainingBounds.map(b => b.y + b.height));

            const combinedBounds = { x: minX, y: minY, width: maxX - minX, height: maxY - minY, index: 99 };
            finalOtherBounds = [combinedBounds];
            userMediaMap[99] = mediaFiles[0]; // Asignar el primer archivo al área fusionada

            console.log('[FUSIONADO] Fondo único creado para 1/4 restante.');

        } else if (distributionScheme === 'three_individual' && mediaFiles.length >= 3) {
            // Caso 2: TRES INDIVIDUALES
            finalOtherBounds = remainingBounds;
            remainingBounds.forEach((bounds, idx) => {
                 // Asignar los archivos 0, 1, 2 a los índices libres 
                 userMediaMap[bounds.index] = mediaFiles[idx];
            });

        } else if (distributionScheme === 'none') {
             finalOtherBounds = []; // No hay ventanas de fondo
        
        } else if (size === '1' && distributionScheme === 'two_halves') {
            // Caso 3: Fusionar 2 y dejar 1 individual (LÓGICA BASADA EN assignmentMap)
            // Se necesita al menos 2 archivos.
            if (mediaFiles.length >= 2) {
                
                // 1. Identificar el índice de la ventana individual (p.ej., 2)
                const individualIndex = parseInt(assignmentMap.individualArea); 
                // 2. Encontrar los bounds de las dos áreas a fusionar
                const boundsToFuse = remainingBounds.filter(b => b.index !== individualIndex);
                // 3. Obtener el bound de la ventana individual restante
                const individualBound = remainingBounds.find(b => b.index === individualIndex);
                
                // 4. Calcular el bound fusionado
                const minX = Math.min(...boundsToFuse.map(b => b.x));
                const minY = Math.min(...boundsToFuse.map(b => b.y));
                const maxX = Math.max(...boundsToFuse.map(b => b.x + b.width));
                const maxY = Math.max(...boundsToFuse.map(b => b.y + b.height));
                
                const combinedBounds = { x: minX, y: minY, width: maxX - minX, height: maxY - minY, index: 98 };
                
                // 5. Definir los bounds finales
                finalOtherBounds = [combinedBounds, individualBound];
                
                // 6. Asignar archivos (el primero al fusionado, el segundo al individual)
                userMediaMap[98] = mediaFiles[0];
                userMediaMap[individualBound.index] = mediaFiles[1];
                
                console.log('[FUSIONADO AVANZADO] Fusionadas 2 áreas y 1 individual restante.');
            }
        }
    } 
    // --- FIN LÓGICA DE DISTRIBUCIÓN AVANZADA ---

    // Cerrar selector
    if (winSelector) {
        winSelector.close();
        winSelector = null;
    }

    // 1. Create main window
    const mainWin = createWindow(mainBounds, true);
    windows.push(mainWin);
    
    // 2. Create background windows (usando el array fusionado o normal)
    finalOtherBounds.forEach((bounds) => {
        const bgWin = createWindow(bounds, false);
        windows.push(bgWin);
    });
    
    // --- GUARDAR CONFIGURACIÓN ---
    saveLastConfig({ 
        size, 
        position, 
        mediaFiles, 
        distributionScheme, 
        assignmentMap 
    });
    // --- FIN GUARDAR CONFIGURACIÓN ---


    // ----------------------
    // Al cargar la ventana principal 
    // ----------------------
    mainWin.webContents.once('did-finish-load', () => {
        
        const bannersTopPath = path.join(imagesDir, config.bannersTopDirName); 
        const bannersBottomPath = path.join(imagesDir, config.bannersBottomDirName); 
        const mobileImgsPath = path.join(imagesDir, config.mobileImgsDirName); 

        // Generar rutas de banners (CLAVE: usar url.pathToFileURL().href)
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
        });

        // Carga inicial
        if (fs.existsSync(userFile)) {
            const text = fs.readFileSync(userFile, 'utf-8');
            mainWin.webContents.send('file-changed', text);
            startInactivityTimer(mainWin); 
        } else {
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

        // Background windows - cargar medios del usuario
        const bgWindows = windows.filter(w => w !== mainWin);
        bgWindows.forEach((bgWin) => {
            bgWin.webContents.once('did-finish-load', () => {
                const positionIndex = bgWin.positionIndex;
                const mediaFilePath = userMediaMap[positionIndex];
                
                if (mediaFilePath && fs.existsSync(mediaFilePath)) {
                    const fileName = path.basename(mediaFilePath);
                    const isVideo = /\.(mp4)$/i.test(fileName);
                    const isGif = /\.(gif)$/i.test(fileName);
                    
                    // --- AJUSTE CLAVE DE RUTA PARA COMPATIBILIDAD CON WINDOWS ---
                    // Reemplazamos barras invertidas por diagonales
                    const sanitizedPath = mediaFilePath.replace(/\\/g, '/');
                    // Generar la URL de archivo segura (file://)
                    const mediaUrl = url.pathToFileURL(sanitizedPath).href;
                    // ------------------------------------------------------------
                    
                    const mediaForWindow = {
                        type: isVideo ? 'video' : isGif ? 'gif' : 'image',
                        src: mediaUrl, // CLAVE: Aquí se pasa la URL segura file://
                        name: fileName,
                        priority: positionIndex
                    };

                    bgWin.webContents.send('load-images', {
                        mediaFiles: [mediaForWindow]
                    });
                }
            });
        });
    });
});


// ----------------------
// App ready - Carga la última configuración o el selector
// ----------------------
app.whenReady().then(() => {
    const lastConfig = loadLastConfig();
    
    if (lastConfig && lastConfig.size) {
        // Usamos process.nextTick para evitar errores de EventEmitter al emitir inmediatamente
        process.nextTick(() => {
            ipcMain.emit('selection-made', null, lastConfig); 
        });
    } else {
        createSelectorWindow();
    }
});

// ----------------------
// Cerrar app (sin cambios)
// ----------------------
app.on('window-all-closed', () => { 
    if (process.platform !== 'darwin') app.quit(); 
});