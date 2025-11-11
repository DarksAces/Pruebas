// JavaScript/windowManager.js

const { app, BrowserWindow } = require('electron');
const path = require('path'); // --- AÑADIDO --- El módulo 'path' para crear rutas de archivo
const appState = require('./appState');
const pathManager = require('./pathManager');
const { clearInactivityTimer } = require('./inactivityManager');

function createSelectorWindow() {
    if (appState.winSelector) return;
    
    const win = new BrowserWindow({
        width: 450, 
        height: 650,
        frame: true,
        resizable: false,
        // --- AÑADIDO --- Ruta a tu icono.
        icon: 'C:\\recursos\\imagenes\\icon\\icon.png',
        webPreferences: {
            preload: pathManager.preloadScript, // Ruta actualizada
            contextIsolation: true,
            nodeIntegration: false
            
        }
        
    });

    // --- AÑADIDO --- Esta línea elimina el menú "File", "Edit", etc.
    win.setMenu(null); 

    win.loadFile(pathManager.selectorHtml); // Ruta actualizada

    win.on('closed', () => {
        appState.winSelector = null;
        if (!appState.windows.length) {
            app.quit();
        }
    });
    
    appState.winSelector = win;
}

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
            preload: pathManager.preloadScript, // Ruta actualizada
            contextIsolation: true,
            webSecurity: false 
        }
    });

    win.setAlwaysOnTop(true, 'screen-saver');
    
    if (isMain) {
        win.loadFile(pathManager.indexHtml); // Ruta actualizada
        win.setIgnoreMouseEvents(false);
        
        // Registrar atajo de teclado para volver al selector
        win.webContents.on('before-input-event', (event, input) => {
            if (input.control && input.shift && input.key.toLowerCase() === 'r') {
                console.log('[ATAJO] Ctrl+Shift+R detectado - Volviendo al selector');
                event.preventDefault();
                
                closeAllWindows();
                clearInactivityTimer();
                createSelectorWindow();
            }
        });
    } else {
        win.loadFile(pathManager.backgroundHtml); // Ruta actualizada
        win.setIgnoreMouseEvents(true);
    }
    
    if (bounds.index !== undefined) {
        win.positionIndex = bounds.index;
    }

    return win;
}

function closeAllWindows() {
    appState.windows.forEach(w => {
        if (!w.isDestroyed()) {
            w.close();
        }
    });
    appState.windows = [];
}

module.exports = {
    createSelectorWindow,
    createWindow,
    closeAllWindows
};
