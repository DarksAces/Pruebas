// JavaScript/main.js (Versión CORREGIDA)

const { app, ipcMain } = require('electron');
const path = require('path');
const configManager = require('./configManager');
const windowManager = require('./windowManager');
const { registerHandlers } = require('./ipcHandlers');
const logManager = require('./logManager'); 

// 1. Cargar configuración
try {
    const configPath = path.join(__dirname, '..', 'config', 'config.json');
    configManager.loadConfig(configPath); 
    console.log('[CONFIG] Archivo de configuración cargado con éxito.');
    
    // Obtener la ruta del DIRECTORIO de log (C:\recursos\log)
    const config = configManager.getConfig(); 
    const logDirPath = config.logFilePath; 
    
    // --- PASOS CLAVE PARA RESOLVER EL ERROR DE PATH ---
    // 1. Inicializar log, pasándole la RUTA DEL DIRECTORIO para que genere el nombre de archivo diario.
    logManager.initializeLog(logDirPath); 
    
    // 2. Ahora que el log está inicializado y limpiado, registramos el inicio de forma segura.
    logManager.log('INFO', 'APP_START', 'Aplicación iniciada. Flujo de logs asegurado.');
    // ---------------------------------------------------

    logManager.log('INFO', 'CONFIG_LOADED', `Configuración cargada. Tiempo de inactividad: ${config.inactivityTimeMs}ms`); 

} catch (error) {
    // Si loadConfig falla, no tenemos logFilePath, por lo que este log es solo consola.
    console.error('[CONFIG FATAL ERROR] No se pudo cargar o parsear config.json. ¡La aplicación no puede continuar!', error);
    
    // Intentamos el log fatal como último recurso, aunque probablemente fallará si la ruta es mala
    logManager.logFatal('MAIN_LOAD_CONFIG', error); 
    app.quit();
    return;
}

// ... (resto del archivo)

// 2. Registrar todos los manejadores IPC
registerHandlers();

// 3. Iniciar la aplicación
app.whenReady().then(() => {
    const lastConfig = configManager.loadLastConfig();
    
    if (lastConfig && lastConfig.size) {
        logManager.log('INFO', 'INIT', `Última configuración encontrada. Recargando modo: ${lastConfig.size}/${lastConfig.position}`); 
        console.log('[INIT] Ultima configuración encontrada, recargando...');
        
        process.nextTick(() => {
            ipcMain.emit('selection-made', null, lastConfig); 
        });
    } else {
        logManager.log('INFO', 'INIT', 'No se encontró última configuración. Abriendo selector.'); 
        console.log('[INIT] No se encontró última configuración, abriendo selector.');
        windowManager.createSelectorWindow();
    }
});

// 4. Manejar cierre
app.on('window-all-closed', () => { 
    if (process.platform !== 'darwin') app.quit(); 
    logManager.log('INFO', 'APP_QUIT', 'Aplicación terminada (window-all-closed).'); 
});