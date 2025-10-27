const { app, BrowserWindow, ipcMain, screen } = require('electron');
const path = require('path');
const fs = require('fs');

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
        width: 400,
        height: 350,
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

    return win;
}

// Update calculatePositions to use display bounds instead of workArea
function calculatePositions(size, selectedPos) {
    const display = screen.getAllDisplays()[1] || screen.getPrimaryDisplay();
    const { width: sw, height: sh, x: sx, y: sy } = display.bounds;
    
    if (size === "3") {
        return {
            mainBounds: { x: sx, y: sy, width: sw, height: sh },
            otherBounds: []
        };
    }
    
    if (size === "2") {
        const isVertical = selectedPos <= 2;
        const mainPos = {
            x: isVertical ? sx + (selectedPos-1)*(sw/2) : sx,
            y: sy,
            width: isVertical ? sw/2 : sw,
            height: sh
        };
        
        const otherPos = {
            x: isVertical ? sx + ((selectedPos === 1) ? sw/2 : 0) : sx,
            y: sy,
            width: isVertical ? sw/2 : sw,
            height: sh
        };

        return { mainBounds: mainPos, otherBounds: [otherPos] };
    }
    
    if (size === "1") {
        const positions = [
            { x: sx, y: sy },               // Top-left
            { x: sx + sw/2, y: sy },        // Top-right
            { x: sx, y: sy + sh/2 },        // Bottom-left
            { x: sx + sw/2, y: sy + sh/2 }  // Bottom-right
        ];
        
        const mainPos = {
            ...positions[selectedPos-1],
            width: sw/2,
            height: sh/2
        };
        
        const others = positions
            .filter((_, i) => i !== selectedPos-1)
            .map(pos => ({
                ...pos,
                width: sw/2,
                height: sh/2
            }));

        return { mainBounds: mainPos, otherBounds: others };
    }
}

// ----------------------
// Leer medios de carpeta
// ----------------------
// Modify the getMediaFiles function to include priority
function getMediaFiles(dir) {
    if (!fs.existsSync(dir)) return [];
    let files = [];
    fs.readdirSync(dir, { withFileTypes: true }).forEach(f => {
        const fullPath = path.join(dir, f.name);
        if (f.isDirectory()) {
            files.push(...getMediaFiles(fullPath));
        } else if (/\.(png|jpe?g|gif|webp|mp4)$/i.test(f.name)) {
            const priority = f.name.charAt(0);
            if (['1','2','3'].includes(priority)) {
                const isVideo = /\.(mp4)$/i.test(f.name);
                const isGif = /\.(gif)$/i.test(f.name);
                files.push({
                    type: isVideo ? 'video' : isGif ? 'gif' : 'image',
                    src: 'file://' + fullPath.replace(/\\/g, '/'),
                    name: f.name,
                    priority: parseInt(priority)
                });
            }
        }
    });
    return files;
}

// ----------------------
// Crear todas las ventanas y cargar contenido
// ----------------------
function createGridWindows(size, position) {
    // Cerrar previas
    windows.forEach(w => w.close());
    windows = [];

    const { mainBounds, otherBounds } = calculatePositions(size, parseInt(position));

    // Create main window
    const mainWin = createWindow(mainBounds, true);
    windows.push(mainWin);

    // Create background windows in correct positions
    otherBounds.forEach((bounds, i) => {
        const bgWin = createWindow(bounds, false);
        windows.push(bgWin);
    });

    // ----------------------
    // Al cargar la ventana principal
    // ----------------------
    mainWin.webContents.on('did-finish-load', () => {
        const allMediaFiles = getMediaFiles(resourcesDir)
            .sort((a, b) => a.priority - b.priority);
        
        // Get banners
        const bannersTop = fs.existsSync(path.join(imagesDir,'BannersTop')) 
            ? fs.readdirSync(path.join(imagesDir,'BannersTop'))
                .filter(f => /\.(png|jpe?g|gif|webp)$/i.test(f))
                .map(f => 'file://' + path.join(imagesDir,'BannersTop',f)) 
            : [];
        const bannersBottom = fs.existsSync(path.join(imagesDir,'BannersBottom')) 
            ? fs.readdirSync(path.join(imagesDir,'BannersBottom'))
                .filter(f => /\.(png|jpe?g|gif|webp)$/i.test(f))
                .map(f => 'file://' + path.join(imagesDir,'BannersBottom',f)) 
            : [];
        const mobileImgs = fs.existsSync(path.join(imagesDir,'Moviles')) 
            ? fs.readdirSync(path.join(imagesDir,'Moviles'))
                .filter(f => /\.(png|jpe?g|gif|webp)$/i.test(f))
                .map(f => 'file://' + path.join(imagesDir,'Moviles',f)) 
            : [];

        // File watcher for content.txt
        const watcher = fs.watch(resourcesDir, (eventType, filename) => {
            if (filename === 'contenido.txt') {
                if (!fs.existsSync(userFile)) {
                    mainWin.webContents.send('no-file', { 
                        welcomePath: 'file://' + welcomeImage 
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
            mainWin.webContents.send('load-images', {
                bannersTop,
                bannersBottom,
                mobileImgs,
                mediaFiles: []
            });
        } else {
            mainWin.webContents.send('no-file', { 
                welcomePath: 'file://' + welcomeImage 
            });
        }

        // Background windows
        const bgWindows = windows.filter(w => w !== mainWin);
        bgWindows.forEach((bgWin, i) => {
            bgWin.webContents.once('did-finish-load', () => {
                const mediaForWindow = allMediaFiles.filter(m => m.priority === (i + 1));
                if (mediaForWindow.length > 0) {
                    bgWin.webContents.send('load-images', {
                        mediaFiles: [mediaForWindow[0]]
                    });
                }
            });
        });
    });

    // Cerrar selector
    if (winSelector) {
        winSelector.close();
        winSelector = null;
    }
}

// ----------------------
// IPC
// ----------------------
ipcMain.on('selection-made', (e, { size, position }) => createGridWindows(size, position));

// ----------------------
// App ready
// ----------------------
app.whenReady().then(createSelectorWindow);

// ----------------------
// Cerrar app
// ----------------------
app.on('window-all-closed', () => { if (process.platform !== 'darwin') app.quit(); });
