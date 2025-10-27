const { app, BrowserWindow, ipcMain, screen } = require('electron');
const path = require('path');
const fs = require('fs');

let winSelector;
let windows = []; // Todas las ventanas (principal + fondo)

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
// Crear ventana (principal o fondo)
// ----------------------
function createWindow(bounds, isMain = false) {
    const win = new BrowserWindow({
        x: bounds.x,
        y: bounds.y,
        width: bounds.width,
        height: bounds.height,
        frame: false,
        resizable: false,
        alwaysOnTop: isMain,
        backgroundColor: '#1e1e1e',
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
            contextIsolation: true
        }
    });

    if (isMain) win.loadFile(path.join(htmlDir, 'index.html'));
    else win.loadFile(path.join(htmlDir, 'background.html'));

    return win;
}

// ----------------------
// Calcular posiciones según tamaño y posición elegida
// ----------------------
function calculatePositions(size, selectedPos) {
    const display = screen.getAllDisplays()[1] || screen.getPrimaryDisplay();
    const { width: sw, height: sh, x: sx, y: sy } = display.bounds;

    let positions = [];

    if (size === "3") {
        positions.push({ x: sx, y: sy, width: sw, height: sh });
    } else if (size === "2") {
        positions = [
            { x: sx, y: sy, width: sw/2, height: sh },
            { x: sx + sw/2, y: sy, width: sw/2, height: sh },
            { x: sx, y: sy, width: sw, height: sh/2 },
            { x: sx, y: sy + sh/2, width: sw, height: sh/2 }
        ];
    } else if (size === "1") {
        positions = [
            { x: sx, y: sy, width: sw/2, height: sh/2 },
            { x: sx + sw/2, y: sy, width: sw/2, height: sh/2 },
            { x: sx, y: sy + sh/2, width: sw/2, height: sh/2 },
            { x: sx + sw/2, y: sy + sh/2, width: sw/2, height: sh/2 }
        ];
    }

    return {
        mainBounds: positions[selectedPos-1],
        otherBounds: positions.filter((_,i)=>i!==selectedPos-1)
    };
}

// ----------------------
// Crear todas las ventanas y cargar contenido
// ----------------------
function createGridWindows(size, position) {
    // Cerrar previas
    windows.forEach(w => w.close());
    windows = [];

    const { mainBounds, otherBounds } = calculatePositions(size, parseInt(position));

    // Ventana principal
    const mainWin = createWindow(mainBounds, true);
    windows.push(mainWin);

    // Ventanas de fondo
    otherBounds.forEach(bounds => {
        const bgWin = createWindow(bounds, false);
        windows.push(bgWin);
    });

    // Enviar datos al cargar la ventana principal
    mainWin.webContents.on('did-finish-load', () => {

        // 1️⃣ Contenido TXT
        if (fs.existsSync(userFile)) {
            const text = fs.readFileSync(userFile, 'utf-8');
            mainWin.webContents.send('file-changed', text);

            // Monitorear cambios
            fs.watch(userFile, (eventType) => {
                if (eventType === 'change') {
                    const updatedText = fs.readFileSync(userFile, 'utf-8');
                    mainWin.webContents.send('file-changed', updatedText);
                }
            });
        } else {
            mainWin.webContents.send('no-file', { welcomePath: 'file://' + welcomeImage });
        }

        // 2️⃣ Cargar imágenes y videos, priorizando por nombre
        let mediaFiles = [];

        if (fs.existsSync(imagesDir)) {
            mediaFiles.push(...fs.readdirSync(imagesDir)
                .filter(f => /\.(png|jpe?g|gif|webp)$/i.test(f))
                .map(f => ({ type: 'img', path: path.join(imagesDir,f), name: f }))
            );
        }

        if (fs.existsSync(videosDir)) {
            mediaFiles.push(...fs.readdirSync(videosDir)
                .filter(f => /\.mp4$/i.test(f))
                .map(f => ({ type: 'video', path: path.join(videosDir,f), name: f }))
            );
        }

        // Ordenar por prioridad: 1=alta, 2=media, 3=baja
        mediaFiles.sort((a,b) => parseInt(a.name[0]) - parseInt(b.name[0]));

        mainWin.webContents.send('load-images', mediaFiles);
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
ipcMain.on('selection-made', (e, { size, position }) => {
    createGridWindows(size, position);
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
