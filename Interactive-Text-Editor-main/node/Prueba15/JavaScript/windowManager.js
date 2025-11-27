// JavaScript/windowManager.js

const { app, BrowserWindow } = require('electron');
const path = require('path');
const appState = require('./appState');
const pathManager = require('./pathManager');
const { clearInactivityTimer } = require('./inactivityManager');
// Importación añadida
const logManager = require('./logManager'); 


function createSelectorWindow() {
    if (appState.winSelector) return;
    
    try {
        const win = new BrowserWindow({
            width: 450, 
            height: 650,
            frame: true,
            resizable: false,
            webPreferences: {
                preload: pathManager.preloadScript, 
                contextIsolation: true,
                nodeIntegration: false
            }
        });

        win.setMenu(null); 
        win.loadFile(pathManager.selectorHtml); 

        win.on('closed', () => {
            appState.winSelector = null;
            if (!appState.windows.length) {
                app.quit();
                logManager.log('INFO', 'SELECTOR_CLOSED', 'Selector cerrado. Saliendo de la aplicación.');
            }
        });
        
        appState.winSelector = win;

    } catch (error) {
        logManager.logFatal('WINDOW_CREATE_SELECTOR', error);
        console.error('[FATAL] No se pudo crear la ventana del selector.', error);
        // Si no podemos crear el selector, salimos de la app.
        app.quit(); 
    }
}

function createWindow(bounds, isMain = false) {
    try {
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
                preload: pathManager.preloadScript, 
                contextIsolation: true,
                webSecurity: false 
            }
        });

        win.setAlwaysOnTop(true, 'screen-saver');
        
        if (isMain) {
            win.loadFile(pathManager.indexHtml); 
            win.setIgnoreMouseEvents(false);
            
            win.webContents.on('before-input-event', (event, input) => {
                if (input.control && input.shift && input.key.toLowerCase() === 'r') {
                    console.log('[ATAJO] Ctrl+Shift+R detectado - Volviendo al selector');
                    event.preventDefault();
                    
                    closeAllWindows();
                    clearInactivityTimer();
                    createSelectorWindow();
                    logManager.log('INFO', 'SHORTCUT_RESET', 'Usuario reseteado por Ctrl+Shift+R.');
                }
            });
        } else {
            win.loadFile(pathManager.backgroundHtml); 
            win.setIgnoreMouseEvents(true);
        }
        
        if (bounds.index !== undefined) {
            win.positionIndex = bounds.index;
        }

        return win;

    } catch (error) {
        logManager.logFatal(`WINDOW_CREATE_${isMain ? 'MAIN' : 'BACKGROUND'}`, error);
        console.error(`[FATAL] No se pudo crear la ventana ${isMain ? 'PRINCIPAL' : 'FONDO'}.`, error);
        throw error; // Lanzar de nuevo para que ipcHandlers la capture si es necesario.
    }
}

function closeAllWindows() {
    try {
        appState.windows.forEach(w => {
            if (!w.isDestroyed()) {
                w.close();
            }
        });
        appState.windows = [];
    } catch (error) {
        logManager.logError('WINDOW_CLOSE_ALL', error);
        console.error('[ERROR] Error al intentar cerrar todas las ventanas.', error);
    }
}

module.exports = {
    createSelectorWindow,
    createWindow,
    closeAllWindows
};