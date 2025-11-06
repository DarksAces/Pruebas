const { app, ipcMain } = require('electron');
const path = require('path');
const configManager = require('./configManager');
const windowManager = require('./windowManager');
const { registerHandlers } = require('./ipcHandlers');

// 1. Cargar configuracion y obtener ruta del icono (AHORA SIMPLIFICADO)
let appIconPath = null;
let appConfig = null;

// La inicialización se realiza aquí, sin pasar rutas.
appConfig = configManager.init();

if (appConfig) {
    console.log('[CONFIG] Inicialización de configuración completada.');

    // Usar la configuración cargada para resolver el icono (si es necesario)
    if (appConfig.resourcesDir && appConfig.iconPath) {
        // En un entorno empaquetado, las rutas de recursos deben ser absolutas
        // windowManager.js será el encargado de manejar el path para el ícono.
        // Aquí solo registramos la configuración.
        appIconPath = appConfig.iconPath;
        console.log(`[ICON] Ruta de icono de configuración: ${appIconPath}`);
    } else {
        console.warn('[ICON] La ruta del icono no se encontro o es incompleta en la configuracion.');
    }
} else {
    // Si configManager.init() falla fatalmente (lo cual no debería con la nueva lógica),
    // la configuración será null o DEFAULT_CONFIG. Manejar el caso de fallo aquí si es crítico.
    console.error('[CONFIG FATAL ERROR] Fallo critico en la inicialización de la configuración.');
    // Mantenemos la aplicación abierta con la configuración por defecto para diagnóstico,
    // a menos que sea absolutamente imposible continuar.
}

// 2. Registrar todos los manejadores IPC
registerHandlers();

// --- FUNCIÓN: Implementacion del cierre seguro ---
function registerCloseHandler() {
    const mainWindow = windowManager.getMainWindow(); 

    if (!mainWindow || mainWindow.isDestroyed()) {
        console.warn('[CLOSE HANDLER] No se pudo obtener la ventana principal para registrar el manejador de cierre.');
        return;
    }

    mainWindow.on('close', (event) => {
        event.preventDefault(); 
        
        console.log('[MAIN] Ventana a punto de cerrarse, notificando al Renderer para guardar.');
        
        mainWindow.webContents.send('app-about-to-close'); 
    });

    ipcMain.once('renderer-save-complete', () => {
        console.log('[MAIN] Renderer confirmo el guardado. Permitiendo cierre.');
        const win = windowManager.getMainWindow();
        
        if (win && !win.isDestroyed()) {
            win.removeAllListeners('close');
            win.close(); 
        } else {
            app.quit();
        }
    });
}
// -----------------------------------------------------------------------------------------

// 3. Iniciar la aplicacion
app.whenReady().then(() => {
    // La configuración ya fue inicializada, solo la recuperamos.
    const finalConfig = configManager.getConfig(); 
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