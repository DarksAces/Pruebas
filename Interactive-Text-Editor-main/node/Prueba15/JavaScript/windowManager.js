// JavaScript/windowManager.js

const { app, BrowserWindow } = require('electron'); 
const path = require('path');
const appState = require('./appState'); 
const pathManager = require('./pathManager'); 
const { clearInactivityTimer } = require('./inactivityManager'); 
const logManager = require('./logManager'); 

/**
 * Crea la ventana del SELECTOR (Configuración inicial).
 * Es una ventana estándar con marco y título.
 */
function createSelectorWindow() {
    if (appState.winSelector) return; // Evitar duplicados
    
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

        win.setMenu(null); // Sin menú superior
        win.loadFile(pathManager.selectorHtml); 

        win.on('closed', () => {
            appState.winSelector = null;
            // Si cerramos el selector y no hay ventanas de contenido, salimos de la app.
            if (!appState.windows.length) {
                app.quit();
                logManager.log('INFO', 'SELECTOR_CLOSED', 'Selector cerrado. Saliendo de la aplicación.');
            }
        });
        
        appState.winSelector = win;

    } catch (error) {
        logManager.logFatal('WINDOW_CREATE_SELECTOR', error);
        console.error('[FATAL] No se pudo crear la ventana del selector.', error);
        app.quit(); 
    }
}

/**
 * Crea ventanas de CONTENIDO (Video o Fondo).
 * @param {Object} bounds - {x, y, width, height, index}
 * @param {boolean} isMain - TRUE si es la ventana principal (interactiva), FALSE si es fondo.
 */
function createWindow(bounds, isMain = false) {
    try {
        console.log(`[VENTANA] Creando ventana ${isMain ? 'PRINCIPAL' : 'FONDO'} en:`, bounds);
        
        const isTransparent = !isMain; // Solo los fondos necesitan transparencia para formas irregulares

        const win = new BrowserWindow({
            x: bounds.x,
            y: bounds.y,
            width: bounds.width,
            height: bounds.height,
            frame: false,            // Sin bordes (modo Kiosco)
            transparent: isTransparent, 
            resizable: false,        
            focusable: isMain,       // Solo la principal recibe teclado/mouse
            skipTaskbar: !isMain,    // Fondos ocultos en barra de tareas
            backgroundColor: '#000000', 
            hasShadow: false,        
            webPreferences: {
                preload: pathManager.preloadScript, 
                contextIsolation: true,
                webSecurity: false   // Permite cargar recursos locales
            }
        });

        // ---------------------------------------------------------------------------
        // Z-ORDERING (Capas de Ventanas)
        // ---------------------------------------------------------------------------
        if (isMain) {
            // 'screen-saver': Nivel más alto. El video siempre flota ENCIMA de todo.
            win.setAlwaysOnTop(true, 'screen-saver'); 
        } else {
            // 'floating': Alto, pero debajo de 'screen-saver'.
            // Los fondos flotan sobre el escritorio pero bajo el video.
            win.setAlwaysOnTop(true, 'floating'); 
        }
        
        // Configuración específica Video Principal
        if (isMain) {
            win.loadFile(pathManager.indexHtml); 
            win.setIgnoreMouseEvents(false); // Interactiva
            
            // --- ATAJO DE EMERGENCIA (Ctrl + Shift + R) ---
            // Permite reiniciar la app si se queda atascada en pantalla completa
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
        } 
        // Configuración específica Fondos
        else {
            win.loadFile(pathManager.backgroundHtml); 
            // Los clics "atraviesan" la ventana (Click-through)
            win.setIgnoreMouseEvents(true);
        }
        
        if (bounds.index !== undefined) {
            win.positionIndex = bounds.index;
        }

        return win;

    } catch (error) {
        logManager.logFatal(`WINDOW_CREATE_${isMain ? 'MAIN' : 'BACKGROUND'}`, error);
        console.error(`[FATAL] No se pudo crear la ventana ${isMain ? 'PRINCIPAL' : 'FONDO'}.`, error);
        throw error; 
    }
}

/**
 * Cierra limpiamente todas las ventanas de contenido.
 */
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