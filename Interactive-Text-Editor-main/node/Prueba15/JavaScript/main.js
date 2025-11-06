// JavaScript/main.js

const { app, ipcMain } = require('electron');
const path = require('path');
const configManager = require('./configManager');
const windowManager = require('./windowManager');
const { registerHandlers } = require('./ipcHandlers');

// 1. Cargar configuracion y obtener ruta del icono
let appIconPath = null;

try {
    const configPath = path.join(__dirname, '..', 'config', 'config.json');
    configManager.loadConfig(configPath);
    console.log('[CONFIG] Archivo de configuracion cargado con exito.');
    
    // Solo para log: windowManager.js se encarga de resolver y aplicar el icono.
    const configData = configManager.getConfig(); 
    if (configData && configData.resourcesDir && configData.iconPath) {
        appIconPath = path.join(configData.resourcesDir, configData.iconPath);
        console.log(`[ICON] Ruta de icono resuelta: ${appIconPath}`);
    } else {
        console.warn('[ICON] La ruta del icono no se encontro en la configuracion.');
    }

} catch (error) {
    console.error('[CONFIG FATAL ERROR] No se pudo cargar o parsear config.json. ¡La aplicacion no puede continuar!', error);
    app.quit();
    return; // Salir del script si la config falla
}

// 2. Registrar todos los manejadores IPC
registerHandlers();

// --- FUNCIÓN: Implementacion del cierre seguro (Para guardar localStorage antes de cerrar) ---
function registerCloseHandler() {
    const mainWindow = windowManager.getMainWindow(); 

    if (!mainWindow || mainWindow.isDestroyed()) {
        console.warn('[CLOSE HANDLER] No se pudo obtener la ventana principal para registrar el manejador de cierre.');
        return;
    }

    // Prevenir que la ventana se cierre inmediatamente
    mainWindow.on('close', (event) => {
        event.preventDefault(); 
        
        console.log('[MAIN] Ventana a punto de cerrarse, notificando al Renderer para guardar.');
        
        // Enviar senal al Renderer (index.html)
        mainWindow.webContents.send('app-about-to-close'); 
    });

    // Esperar la confirmacion del Renderer
    ipcMain.once('renderer-save-complete', () => {
        console.log('[MAIN] Renderer confirmo el guardado. Permitiendo cierre.');
        const win = windowManager.getMainWindow();
        
        // Desactivar el listener 'close' para que la llamada a .close() no se prevenga
        if (win && !win.isDestroyed()) {
            win.removeAllListeners('close');
            win.close(); // Cerrar la ventana finalmente
        } else {
            app.quit();
        }
    });
}
// -----------------------------------------------------------------------------------------

// 3. Iniciar la aplicacion
app.whenReady().then(() => {
    const lastConfig = configManager.loadLastConfig();

    if (lastConfig && lastConfig.size) {
        console.log('[INIT] Ultima configuracion encontrada, recargando...');

        process.nextTick(() => {
            ipcMain.emit('selection-made', null, lastConfig); 
            // Registrar el manejador de cierre seguro
            registerCloseHandler();
    });
    } else {
        console.log('[INIT] No se encontro ultima configuracion, abriendo selector.');
        windowManager.createSelectorWindow();
    }
});

// 4. Manejar cierre
app.on('window-all-closed', () => { 
    if (process.platform !== 'darwin') app.quit(); 
});