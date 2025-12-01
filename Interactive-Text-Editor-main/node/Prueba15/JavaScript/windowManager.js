// JavaScript/windowManager.js

// Importamos los módulos necesarios de Electron y de nuestro proyecto.
const { app, BrowserWindow } = require('electron'); // BrowserWindow es la clase para crear ventanas
const path = require('path');
const appState = require('./appState'); // Gestiona el estado global (ventanas abiertas, timers)
const pathManager = require('./pathManager'); // Centraliza todas las rutas de archivos
const { clearInactivityTimer } = require('./inactivityManager'); // Para resetear el timer al cerrar
const logManager = require('./logManager'); // Sistema de registro de logs

/**
 * Crea la ventana del SELECTOR inicial.
 * Esta es la ventana con marco y botones donde eliges la configuración (1, 2, 3 pantallas).
 */
function createSelectorWindow() {
    // Si ya existe el selector, no creamos otro para evitar duplicados.
    if (appState.winSelector) return;
    
    try {
        // Definimos las propiedades visuales de la ventana
        const win = new BrowserWindow({
            width: 450, 
            height: 650,
            frame: true,     // 'true' = Tiene barra de título y borde (estilo ventana normal)
            resizable: false,// 'false' = El usuario no puede cambiarle el tamaño arrastrando
            webPreferences: {
                preload: pathManager.preloadScript, // Script puente entre Node.js y el HTML
                contextIsolation: true, // SEGURIDAD: Aísla el contexto de la web del de Node
                nodeIntegration: false  // SEGURIDAD: El HTML no puede usar 'require' directamente
            }
        });

        win.setMenu(null); // Eliminamos la barra de menú estándar de Windows (Archivo, Editar...)
        win.loadFile(pathManager.selectorHtml); // Cargamos el HTML del selector

        // Evento: Cuando el usuario cierra esta ventana (con la X)
        win.on('closed', () => {
            appState.winSelector = null;
            // Si no quedan otras ventanas abiertas (ni video ni fondos), cerramos la App completa.
            if (!appState.windows.length) {
                app.quit();
                logManager.log('INFO', 'SELECTOR_CLOSED', 'Selector cerrado. Saliendo de la aplicación.');
            }
        });
        
        // Guardamos la referencia en el estado global
        appState.winSelector = win;

    } catch (error) {
        // Si falla, registramos el error fatal y cerramos todo por seguridad
        logManager.logFatal('WINDOW_CREATE_SELECTOR', error);
        console.error('[FATAL] No se pudo crear la ventana del selector.', error);
        app.quit(); 
    }
}

/**
 * Crea las ventanas de CONTENIDO (Video principal o Fondos de relleno).
 * @param {Object} bounds - Coordenadas y tamaño {x, y, width, height, index}
 * @param {boolean} isMain - TRUE si es la ventana del video, FALSE si es fondo.
 */
function createWindow(bounds, isMain = false) {
    try {
        console.log(`[VENTANA] Creando ventana ${isMain ? 'PRINCIPAL' : 'FONDO'} en:`, bounds);
        
        // Solo las ventanas de fondo necesitan transparencia real en Electron
        const isTransparent = !isMain; 

        // Configuración avanzada de la ventana
        const win = new BrowserWindow({
            x: bounds.x,
            y: bounds.y,
            width: bounds.width,
            height: bounds.height,
            frame: false,            // 'false' = Sin bordes ni barra de título (modo kiosco/pantalla completa)
            transparent: isTransparent, 
            resizable: false,        // Fijo, no se puede estirar
            focusable: isMain,       // Solo la principal puede recibir foco (teclado/mouse)
            skipTaskbar: !isMain,    // Los fondos no aparecen en la barra de tareas de Windows
            backgroundColor: '#000000', // Fondo negro base para evitar destellos blancos al cargar
            hasShadow: false,        // Sin sombras de sistema operativo
            webPreferences: {
                preload: pathManager.preloadScript, 
                contextIsolation: true,
                webSecurity: false   // 'false' = Permite cargar imágenes locales (file://) sin bloqueos
            }
        });

        // ---------------------------------------------------------------------------
        // SOLUCIÓN AL PROBLEMA DE "Z-ORDER" (SUPERPOSICIÓN)
        // Aquí le decimos a Windows qué ventana pintar encima de cuál.
        // ---------------------------------------------------------------------------
        if (isMain) {
            // NIVEL: screen-saver (Máximo)
            // Ponemos el video en el nivel más alto posible del sistema.
            // Esto garantiza que flote SOBRE los fondos, incluso si se solapan.
            win.setAlwaysOnTop(true, 'screen-saver'); 
        } else {
            // NIVEL: floating (Alto, pero menor que screen-saver)
            // Los fondos flotan sobre el escritorio, pero siempre DEBAJO del video.
            // Así evitamos que un fondo tape accidentalmente al video.
            win.setAlwaysOnTop(true, 'floating'); 
        }
        // ---------------------------------------------------------------------------
        
        // Lógica específica si es la Ventana Principal (VIDEO)
        if (isMain) {
            win.loadFile(pathManager.indexHtml); 
            win.setIgnoreMouseEvents(false); // Esta ventana SÍ debe detectar clics y teclado
            
            // --- ATAJO DE TECLADO OCULTO (Ctrl + Shift + R) ---
            // Escuchamos eventos de teclado antes de que lleguen a la web
            win.webContents.on('before-input-event', (event, input) => {
                if (input.control && input.shift && input.key.toLowerCase() === 'r') {
                    console.log('[ATAJO] Ctrl+Shift+R detectado - Volviendo al selector');
                    event.preventDefault(); // Evitamos cualquier acción por defecto del navegador
                    
                    // Reiniciamos la aplicación al estado inicial
                    closeAllWindows();
                    clearInactivityTimer();
                    createSelectorWindow();
                    logManager.log('INFO', 'SHORTCUT_RESET', 'Usuario reseteado por Ctrl+Shift+R.');
                }
            });
        } 
        // Lógica específica si es una Ventana de Fondo
        else {
            win.loadFile(pathManager.backgroundHtml); 
            // IMPORTANTE: 'setIgnoreMouseEvents(true)' hace que los clics "atraviesen" 
            // la ventana. El usuario no puede interactuar con el fondo, es como un fantasma visual.
            win.setIgnoreMouseEvents(true);
        }
        
        // Guardamos el índice de posición (1, 2, 3, 4) dentro del objeto ventana
        // para saber qué imagen cargar después.
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
 * Cierra TODAS las ventanas de contenido (Video y Fondos).
 * Se usa cuando volvemos al selector o cerramos la app.
 */
function closeAllWindows() {
    try {
        // Iteramos sobre el array de ventanas guardadas en el estado
        appState.windows.forEach(w => {
            // Verificamos que la ventana no haya sido destruida ya por el usuario
            if (!w.isDestroyed()) {
                w.close();
            }
        });
        // Limpiamos el array para dejarlo vacío
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