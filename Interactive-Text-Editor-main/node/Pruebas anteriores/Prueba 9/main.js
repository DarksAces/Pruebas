// main.js
const { app, BrowserWindow, ipcMain, screen } = require('electron');
const path = require('path');
const fs = require('fs');

let winSelector;
let winMain;
let winBackground;

const htmlDir = path.join(__dirname, 'html');
const resourcesDir = path.join(__dirname, 'recursos');
const imagesDir = path.join(resourcesDir, 'imagenes');
const userFile = path.join(resourcesDir, 'contenido.txt');
const welcomeImage = path.join(imagesDir, 'Bienvenida', 'welcome.png');

// ----------------------
// Ventana selector
// ----------------------
function createSelectorWindow() {
    winSelector = new BrowserWindow({
        width: 400,
        height: 300,
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
// Ventana fondo (video)
// ----------------------
function createBackgroundWindow(displayBounds) {
    const { x, y, width, height } = displayBounds;

    winBackground = new BrowserWindow({
        x, y, width, height,
        frame: false,
        resizable: false,
        alwaysOnTop: false,
        webPreferences: {
            contextIsolation: true,
            nodeIntegration: false
        }
    });

    winBackground.loadFile(path.join(htmlDir, 'background.html'));
    winBackground.setAlwaysOnTop(false, 'screen-saver');
}

// ----------------------
// Ventana principal
// ----------------------
function createMainWindow(size, position) {
    const displays = screen.getAllDisplays();
    const selectedDisplay = displays[1] || screen.getPrimaryDisplay();
    const { width: sw, height: sh, x: screenX, y: screenY } = selectedDisplay.bounds;

    let width, height, x, y;

    if (size === "3") {
        width = sw; height = sh; x = screenX; y = screenY;
    } else if (size === "2") {
        switch(position) {
            case "1": x = screenX; y = screenY; width = sw/2; height = sh; break;
            case "2": x = screenX + sw/2; y = screenY; width = sw/2; height = sh; break;
            case "3": x = screenX; y = screenY; width = sw; height = sh/2; break;
            case "4": x = screenX; y = screenY + sh/2; width = sw; height = sh/2; break;
        }
    } else if (size === "1") {
        width = sw/2; height = sh/2;
        switch(position) {
            case "1": x = screenX; y = screenY; break;
            case "2": x = screenX + sw/2; y = screenY; break;
            case "3": x = screenX; y = screenY + sh/2; break;
            case "4": x = screenX + sw/2; y = screenY + sh/2; break;
        }
    }

    // Crear ventana de fondo si no existe
    if (!winBackground) {
        createBackgroundWindow(selectedDisplay.bounds);
    }

    // Crear ventana principal encima
    winMain = new BrowserWindow({
        x, y, width, height,
        frame: false,
        resizable: false,
        alwaysOnTop: true,
        backgroundColor: '#1e1e1e',
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
            contextIsolation: true,
            nodeIntegration: false
        }
    });

    winMain.loadFile(path.join(htmlDir, 'index.html'));

    if (winSelector) {
        winSelector.close();
        winSelector = null;
    }

    // ----------------------
    // Enviar datos al cargar
    // ----------------------
    winMain.webContents.on('did-finish-load', () => {

        // 1️⃣ Contenido txt
        if (fs.existsSync(userFile)) {
            const text = fs.readFileSync(userFile, 'utf-8');
            winMain.webContents.send('file-changed', text);
        } else {
            winMain.webContents.send('no-file', { welcomePath: 'file://' + welcomeImage });
        }

        // 2️⃣ Vigilar cambios en tiempo real
        fs.watch(userFile, (eventType) => {
            if (eventType === 'change') {
                const updatedText = fs.readFileSync(userFile, 'utf-8');
                winMain.webContents.send('file-changed', updatedText);
            }
        });

        // 3️⃣ Cargar imágenes
        if (fs.existsSync(imagesDir)) {
            const allImages = fs.readdirSync(imagesDir).filter(f => /\.(png|jpe?g|gif|webp)$/i.test(f));
            const bannersTop = allImages.filter(f => f.startsWith('top_')).map(f => 'file://' + path.join(imagesDir, f));
            const bannersBottom = allImages.filter(f => f.startsWith('bottom_')).map(f => 'file://' + path.join(imagesDir, f));
            const mobileImgs = allImages.filter(f => f.startsWith('mobile_')).map(f => 'file://' + path.join(imagesDir, f));

            winMain.webContents.send('load-images', { bannersTop, bannersBottom, mobileImgs });
        }
    });
}

// ----------------------
// IPC
// ----------------------
ipcMain.on('selection-made', (e, { size, position }) => {
    createMainWindow(size, position);
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
