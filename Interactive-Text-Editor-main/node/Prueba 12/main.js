// main.js

const { app, BrowserWindow, ipcMain, screen, dialog } = require('electron');
const path = require('path');
const fs = require('fs');
const url = require('url'); 

let winSelector;
let windows = [];

const htmlDir = path.join(__dirname, 'html');
const resourcesDir = path.join(__dirname, 'recursos');
const imagesDir = path.join(resourcesDir, 'imagenes');
const videosDir = path.join(resourcesDir, 'video');
const userFile = path.join(resourcesDir, 'contenido.txt');
const welcomeImage = path.join(imagesDir, 'Bienvenida', 'welcome.png');

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

    win.setAlwaysOnTop(true, 'screen-saver');
    win.moveTop();

    if (isMain) {
        win.loadFile(path.join(htmlDir, 'index.html'));
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
        message: `Selecciona hasta ${maxFiles} archivos de imagen o video.`
    });

    if (result.canceled) {
        return null;
    }
    return result.filePaths;
});

// Update calculatePositions para retornar el índice de posición absoluta (1-4)
function calculatePositions(size, selectedPos) {
    const display = screen.getAllDisplays()[1] || screen.getPrimaryDisplay();
    const { width: sw, height: sh, x: sx, y: sy } = display.bounds;
    
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
        // 1/4 de pantalla: Usamos asignación secuencial si no hay posiciones explícitas (que ya no se piden)
        if (Object.keys(imagePositions).length === 0) { 
            mediaFiles.forEach((filePath, idx) => {
                // otherBounds contiene las 3 posiciones de fondo disponibles.
                if (idx < otherBounds.length) {
                    userMediaMap[otherBounds[idx].index] = filePath;
                }
            });
        } else {
             // Lógica de asignación explícita (mantenida por si acaso)
            Object.keys(imagePositions).forEach(filePath => {
                const pos = parseInt(imagePositions[filePath]);
                userMediaMap[pos] = filePath;
            });
        }
    } else if (size === '2' && otherBounds.length > 0) {
        // 1/2 pantalla: asignar el primer archivo secuencialmente a la única ventana de fondo
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
        
        // Cargar banners y móviles desde el disco 
        const bannersTop = fs.existsSync(path.join(imagesDir,'BannersTop')) 
            ? fs.readdirSync(path.join(imagesDir,'BannersTop'))
                .filter(f => /\.(png|jpe?g|gif|webp)$/i.test(f))
                .map(f => url.pathToFileURL(path.join(imagesDir,'BannersTop',f)).href) 
            : [];
        const bannersBottom = fs.existsSync(path.join(imagesDir,'BannersBottom')) 
            ? fs.readdirSync(path.join(imagesDir,'BannersBottom'))
                .filter(f => /\.(png|jpe?g|gif|webp)$/i.test(f))
                .map(f => url.pathToFileURL(path.join(imagesDir,'BannersBottom',f)).href) 
            : [];
        const mobileImgs = fs.existsSync(path.join(imagesDir,'Moviles')) 
            ? fs.readdirSync(path.join(imagesDir,'Moviles'))
                .filter(f => /\.(png|jpe?g|gif|webp)$/i.test(f))
                .map(f => url.pathToFileURL(path.join(imagesDir,'Moviles',f)).href) 
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
        
        // Enviar la carga de imágenes (banners/móviles) a la ventana principal
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