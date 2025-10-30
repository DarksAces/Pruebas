// main.js

const { app, BrowserWindow, ipcMain, screen, dialog } = require('electron');
const path = require('path');
const fs = require('fs');
const url = require('url'); 

let winSelector;
let windows = [];

// ----------------------
// Directorios Absolutos
// ----------------------
// Usamos path.resolve con el formato Windows para máxima compatibilidad.
const resourcesDir = path.resolve('C:\\recursos'); 

// CONSOLA DE DIAGNÓSTICO: Imprimimos la ruta final para verificar
console.log(`[DIAGNÓSTICO] Ruta de recursos resuelta: ${resourcesDir}`);


const htmlDir = path.join(__dirname, 'html'); 
const imagesDir = path.join(resourcesDir, 'imagenes');
const userFile = path.join(resourcesDir, 'contenido.txt');
const welcomeImage = path.join(imagesDir, 'Bienvenida', 'welcome.png');
// ----------------------

// ----------------------
// Ventana selector
// ----------------------
function createSelectorWindow() {
    winSelector = new BrowserWindow({
        width: 450, 
        height: 600,
        frame: true,
        resizable: false,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
            contextIsolation: true,
            nodeIntegration: false
        }
    });
    winSelector.loadFile(path.join(htmlDir, 'selector.html'));
}

// ----------------------
// Crear ventana
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
        // Mantener como true para que la ventana esté siempre encima de las apps
        alwaysOnTop: true, 
        focusable: false,
        backgroundColor: '#00000000',
        hasShadow: false,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
            contextIsolation: true,
            webSecurity: false 
        }
    });

    // Usamos 'normal' para que respete el Z-index del sistema (Taskbar)
    win.setAlwaysOnTop(true, 'normal'); 
    win.moveTop();

    if (isMain) {
        win.loadFile(path.join(htmlDir, 'index.html'));
        // Permitimos interacciones de ratón en la ventana principal (contenido)
        win.setIgnoreMouseEvents(false);
    } else {
        win.loadFile(path.join(htmlDir, 'background.html'));
        // Eliminamos la interacción con el ratón de las ventanas de fondo
        win.setIgnoreMouseEvents(true); 
    }
    
    if (bounds.index) {
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
        // FORZAR RUTA: Usamos la ruta resuelta y robusta
        defaultPath: resourcesDir 
    });

    if (result.canceled) {
        return null;
    }
    return result.filePaths;
});

// Update calculatePositions para retornar el índice de posición absoluta (1-4)
function calculatePositions(size, selectedPos) {
    // Intentamos usar el SEGUNDO monitor (índice 1). Si no existe, usamos el principal.
    const displays = screen.getAllDisplays();
    const targetDisplay = displays.length > 1 ? displays[1] : displays[0];
    
    // Usamos workArea para obtener el área DISPONIBLE sin Taskbar ni menús.
    const { width: sw, height: sh, x: sx, y: sy } = targetDisplay.workArea;

    // --- NUEVO LOG PARA DIAGNÓSTICO DE DIMENSIONES ---
    console.log(`[DIAGNÓSTICO] Monitor de Destino: ${targetDisplay.id}`);
    console.log(`[DIAGNÓSTICO] Área de Trabajo (WorkArea) - X:${sx}, Y:${sy}, W:${sw}, H:${sh}`);
    // --- FIN LOG ---

    // NOTA: Los cálculos de mitad y cuartos ahora se basan en el área de trabajo disponible.
    // Usamos sx y sy para el inicio de las ventanas.
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
             // Las coordenadas inician en sx, sy (inicio del workArea)
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
ipcMain.on('selection-made', (e, { size, position, mediaFiles, imagePositions }) => {
    
    console.log('Recibido:', { size, position, mediaFiles, imagePositions });
    
    // Cerrar previas
    windows.forEach(w => w.close());
    windows = [];

    const { mainBounds, otherBounds } = calculatePositions(size, parseInt(position));

    // Create main window
    const mainWin = createWindow(mainBounds, true);
    windows.push(mainWin);

    // Create background windows
    otherBounds.forEach((bounds) => {
        const bgWin = createWindow(bounds, false);
        windows.push(bgWin);
    });
    
    // Mapear los archivos de usuario a la posición absoluta (1-4)
    const userMediaMap = {}; 

    if (size === '1') {
        // Asignación secuencial a las 3 ventanas de fondo
        mediaFiles.forEach((filePath, idx) => {
            if (idx < otherBounds.length) {
                userMediaMap[otherBounds[idx].index] = filePath;
            }
        });
    } else if (size === '2' && otherBounds.length > 0) {
        // Asignar el primer archivo secuencialmente a la única ventana de fondo
        mediaFiles.forEach((filePath, idx) => {
            if (idx < otherBounds.length) { // otherBounds.length es 1 en este caso
                userMediaMap[otherBounds[idx].index] = filePath;
            }
        });
    } else if (size === '3') {
        // Pantalla completa: no hay ventanas de fondo
    }

    console.log('Mapa de medios:', userMediaMap);

    // Cerrar selector
    if (winSelector) {
        winSelector.close();
        winSelector = null;
    }

    // ----------------------
    // Al cargar la ventana principal
    // ----------------------
    mainWin.webContents.once('did-finish-load', () => {
        
        // --- DIAGNÓSTICO DE CARGA DE BANNERS ---
        console.log(`Ruta base de imágenes: ${imagesDir}`);

        const bannersTopPath = path.join(imagesDir,'BannersTop');
        const bannersBottomPath = path.join(imagesDir,'BannersBottom');
        const mobileImgsPath = path.join(imagesDir,'Moviles');

        if (!fs.existsSync(imagesDir)) {
            console.error(`ERROR: El directorio base de imágenes ${imagesDir} no existe.`);
        }
        if (!fs.existsSync(bannersTopPath)) {
            console.warn(`ADVERTENCIA: Carpeta de Banners Top no encontrada en ${bannersTopPath}`);
        }
        if (!fs.existsSync(bannersBottomPath)) {
            console.warn(`ADVERTENCIA: Carpeta de Banners Bottom no encontrada en ${bannersBottomPath}`);
        }
        if (!fs.existsSync(mobileImgsPath)) {
            console.warn(`ADVERTENCIA: Carpeta de Móviles no encontrada en ${mobileImgsPath}`);
        }
        // --- FIN DIAGNÓSTICO ---


        // Cargar banners y móviles desde el disco 
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


        // File watcher for content.txt 
        const watcher = fs.watch(resourcesDir, (eventType, filename) => {
            if (filename === 'contenido.txt') {
                if (!fs.existsSync(userFile)) {
                    mainWin.webContents.send('no-file', { 
                        welcomePath: url.pathToFileURL(welcomeImage).href 
                    });
                } else if (eventType === 'change') {
                    const text = fs.readFileSync(userFile, 'utf-8');
                    mainWin.webContents.send('file-changed', text);
                    
                    // REENVIAR banners/móviles tras cambio de archivo si es necesario (mantengo la estructura)
                    mainWin.webContents.send('load-images', {
                        bannersTop,
                        bannersBottom,
                        mobileImgs,
                        mediaFiles: []
                    });
                }
            }
        });

        mainWin.on('closed', () => watcher.close());

        // Initial content load
        if (fs.existsSync(userFile)) {
            const text = fs.readFileSync(userFile, 'utf-8');
            mainWin.webContents.send('file-changed', text);
        } else {
            mainWin.webContents.send('no-file', { 
                welcomePath: url.pathToFileURL(welcomeImage).href 
            });
        }
        
        // --- ENVÍO DEL TAMAÑO DE LA VENTANA (NUEVO) ---
        mainWin.webContents.send('window-size-selected', { size: size });
        // ---------------------------------------------
        
        // --- DIAGNÓSTICO DE CONTENIDO ENVIADO ---
        console.log(`Banners Top encontrados (${bannersTop.length}):`, bannersTop.map(u => path.basename(new URL(u).pathname)));
        console.log(`Banners Bottom encontrados (${bannersBottom.length}):`, bannersBottom.map(u => path.basename(new URL(u).pathname)));
        console.log(`Móviles encontrados (${mobileImgs.length}):`, mobileImgs.map(u => path.basename(new URL(u).pathname)));
        // --- FIN DIAGNÓSTICO ---


        // ENVIAR la carga de imágenes (banners/móviles) a la ventana principal
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
                
                console.log(`Ventana en posición ${positionIndex}, archivo: ${mediaFilePath}`);
                
                if (mediaFilePath && fs.existsSync(mediaFilePath)) {
                    const fileName = path.basename(mediaFilePath);
                    const isVideo = /\.(mp4)$/i.test(fileName);
                    const isGif = /\.(gif)$/i.test(fileName);
                    
                    const mediaUrl = url.pathToFileURL(mediaFilePath).href;
                    
                    const mediaForWindow = {
                        type: isVideo ? 'video' : isGif ? 'gif' : 'image',
                        src: mediaUrl, 
                        name: fileName,
                        priority: positionIndex
                    };

                    console.log('Enviando media a ventana:', mediaForWindow);

                    bgWin.webContents.send('load-images', {
                        mediaFiles: [mediaForWindow]
                    });
                } else {
                    console.log(`No hay archivo para posición ${positionIndex}`);
                }
            });
        });
    });
});


// ----------------------
// App ready
// ----------------------
app.whenReady().then(createSelectorWindow);

// ----------------------
// Cerrar app
// ----------------------
app.on('window-all-closed', () => { 
    if (process.platform !== 'darwin') app.quit(); 
});