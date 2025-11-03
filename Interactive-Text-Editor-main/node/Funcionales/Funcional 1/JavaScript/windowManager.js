// JavaScript/windowManager.js

/*
 * Helpers para crear, posicionar y cerrar ventanas BrowserWindow.
 * Funciones exportadas:
 *  - createSelectorWindow(): crea la ventana del selector (UI de configuración)
 *  - createWindow(bounds, isMain=false): crea una ventana (main o fondo) con los bounds proporcionados
 *  - closeAllWindows(): cierra todas las ventanas de appState.windows
 *
 * Notas importantes:
 *  - Las ventanas de fondo se crean transparentes y no reciben eventos de ratón
 *  - La ventana principal (isMain=true) recibe eventos y carga `index.html`
 */

const { app, BrowserWindow } = require('electron');
const appState = require('./appState');
const pathManager = require('./pathManager');
const { clearInactivityTimer } = require('./inactivityManager');

function createSelectorWindow() {
    // Evitar crear más de una instancia del selector
    if (appState.winSelector) return;
    
    const win = new BrowserWindow({
        width: 450, 
        height: 650,
        frame: true,
        resizable: false,
        webPreferences: {
            // Preload script protegido para exponer solo la API necesaria
            preload: pathManager.preloadScript,
            contextIsolation: true,
            nodeIntegration: false
        }
    });
    win.loadFile(pathManager.selectorHtml);

    win.on('closed', () => {
        appState.winSelector = null;
        // Si no hay ventanas activas, cerramos la app
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
            preload: pathManager.preloadScript,
            contextIsolation: true,
            webSecurity: false // Necesario si se cargan file:// y recursos mixtos
        }
    });

    win.setAlwaysOnTop(true, 'screen-saver');
    
    if (isMain) {
        // Ventana principal: carga el index y acepta eventos de teclado
        win.loadFile(pathManager.indexHtml);
        win.setIgnoreMouseEvents(false);
        
        // Registrar atajo de teclado para volver al selector (Ctrl+Shift+R)
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
        // Ventana de fondo: no interacciona con el usuario
        win.loadFile(pathManager.backgroundHtml);
        win.setIgnoreMouseEvents(true);
    }
    
    // Guardar índice de posición (si viene) en la instancia para usarlo luego
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