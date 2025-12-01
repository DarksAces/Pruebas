// JavaScript/main.js (Versión CORREGIDA para ASAR y COMENTADA)

const { app, ipcMain } = require('electron');
const path = require('path');
const fs = require('fs'); 
const configManager = require('./configManager');
const windowManager = require('./windowManager');
const { registerHandlers } = require('./ipcHandlers');
const logManager = require('./logManager'); 

// -----------------------------------------------------------------------------
// 1. FASE DE INICIALIZACIÓN Y CARGA DE CONFIGURACIÓN
// -----------------------------------------------------------------------------
try {
    // --- MANEJO DE CONFIGURACIÓN EN PRODUCCIÓN (.EXE) ---
    // En un ejecutable empaquetado, los archivos internos son de solo lectura.
    // Debemos copiar 'config.json' a AppData para poder modificarlo (guardar última sesión).
    
    const userDataPath = app.getPath('userData'); // C:\Users\Usuario\AppData\Roaming\App
    const persistentConfigPath = path.join(userDataPath, 'config.json');
    const baseConfigPath = path.join(__dirname, '..', 'config', 'config.json');
    
    // Si no existe en AppData, copiamos el archivo original
    if (!fs.existsSync(persistentConfigPath)) {
        console.log('[CONFIG] No se encontró config.json persistente. Copiando desde base...');
        
        if (!fs.existsSync(userDataPath)) {
            fs.mkdirSync(userDataPath, { recursive: true });
        }
        
        fs.copyFileSync(baseConfigPath, persistentConfigPath);
        console.log(`[CONFIG] Copia exitosa a: ${persistentConfigPath}`);
    }
    
    // Cargamos la configuración desde la ubicación editable
    configManager.loadConfig(persistentConfigPath); 
    console.log('[CONFIG] Archivo de configuración cargado con éxito.');
    
    // --- INICIALIZACIÓN DE LOGS ---
    const config = configManager.getConfig(); 
    const logDirPath = config.logFilePath; 
    
    // Preparamos el sistema de logs rotativos
    logManager.initializeLog(logDirPath); 
    
    logManager.log('INFO', 'APP_START', 'Aplicación iniciada. Flujo de logs asegurado.');
    logManager.log('INFO', 'CONFIG_LOADED', `Configuración cargada. Tiempo de inactividad: ${config.inactivityTimeMs}ms`); 

} catch (error) {
    // Error crítico al inicio: Imposible continuar
    console.error('[CONFIG FATAL ERROR] No se pudo cargar config.json.', error);
    logManager.logFatal('MAIN_LOAD_CONFIG', error); 
    app.quit();
    return;
}

// -----------------------------------------------------------------------------
// 2. REGISTRO DE EVENTOS (IPC)
// -----------------------------------------------------------------------------
// Conectamos los listeners que responderán al Frontend
registerHandlers();

// -----------------------------------------------------------------------------
// 3. ARRANQUE DE LA INTERFAZ
// -----------------------------------------------------------------------------
app.whenReady().then(() => {
    // Revisamos si hay una sesión guardada para restaurarla automáticamente
    const lastConfig = configManager.loadLastConfig();
    
    if (lastConfig && lastConfig.size) {
        // MODO RESTAURACIÓN: Saltamos el selector
        logManager.log('INFO', 'INIT', `Restaurando sesión: ${lastConfig.size}/${lastConfig.position}`); 
        console.log('[INIT] Restaurando última configuración...');
        
        process.nextTick(() => {
            // Emitimos evento interno para simular que el usuario eligió lo mismo
            ipcMain.emit('selection-made', null, lastConfig); 
        });
    } else {
        // MODO NUEVO: Abrimos selector
        logManager.log('INFO', 'INIT', 'Sin configuración previa. Abriendo Selector.'); 
        console.log('[INIT] Abriendo selector.');
        windowManager.createSelectorWindow();
    }
});

// -----------------------------------------------------------------------------
// 4. CIERRE DE LA APLICACIÓN
// -----------------------------------------------------------------------------
app.on('window-all-closed', () => { 
    if (process.platform !== 'darwin') app.quit(); 
    logManager.log('INFO', 'APP_QUIT', 'Aplicación terminada.'); 
});