// JavaScript/main.js

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
    // Definimos el nombre exacto del archivo que pides
    const CONFIG_FILENAME = 'InteractiveContentDisplay.json';
    let appBasePath;
    let configPath;

    // LÓGICA DE RUTAS: PRODUCCIÓN vs DESARROLLO
    if (app.isPackaged) {
        // [PRODUCCIÓN - .EXE]
        // appBasePath será la carpeta donde está el ejecutable (ej: C:\Program Files\TuApp\)
        appBasePath = path.dirname(process.execPath);
        
        // Buscamos el JSON justo al lado del .exe
        configPath = path.join(appBasePath, CONFIG_FILENAME);
    } else {
        // [DESARROLLO - npm start]
        // appBasePath será la raíz del proyecto
        appBasePath = path.join(__dirname, '..');
        
        // En desarrollo, buscamos en la carpeta 'config' estándar
        // Nota: Asegúrate de tener el archivo con este nombre en tu carpeta config/
        configPath = path.join(appBasePath, 'config', CONFIG_FILENAME);
    }

    // --- IMPORTANTE: GLOBALIZAR LA RUTA BASE ---
    // Guardamos esta ruta en una variable global para que pathManager.js 
    // sepa dónde buscar la carpeta de recursos (imágenes, txt) más tarde.
    global.APP_BASE_PATH = appBasePath;

    // VERIFICACIÓN Y CARGA
    if (fs.existsSync(configPath)) {
        console.log(`[INIT] Cargando configuración desde: ${configPath}`);
        configManager.loadConfig(configPath); 
    } else {
        // Si no existe, es un error fatal porque la app no sabe qué hacer sin config.
        // En producción, esto pasaría si el usuario borra el archivo.
        const errorMsg = `[FATAL] No se encuentra el archivo de configuración: ${configPath}`;
        console.error(errorMsg);
        
        // Intentamos loguear (aunque sin config, el logManager quizás no sepa dónde escribir aún)
        // pero tiramos el error para detener la ejecución.
        throw new Error(errorMsg);
    }
    
    // --- INICIALIZACIÓN DE LOGS ---
    const config = configManager.getConfig(); 
    
    // Resolvemos la ruta de logs relativa a la carpeta del ejecutable
    // Si config.logFilePath es "logs", se crearán en "C:\Program Files\TuApp\logs"
    const logDirResolved = path.resolve(appBasePath, config.logFilePath);
    
    logManager.initializeLog(logDirResolved); 
    
    logManager.log('INFO', 'APP_START', `Aplicación iniciada. BasePath: ${appBasePath}`);
    logManager.log('INFO', 'CONFIG_LOADED', `Configuración: ${CONFIG_FILENAME}`); 

} catch (error) {
    console.error('[MAIN FATAL ERROR]', error);
    // Si logManager llegó a iniciar, guardamos el error
    try { logManager.logFatal('MAIN_BOOTSTRAP', error); } catch(e){}
    app.quit();
    return;
}

// -----------------------------------------------------------------------------
// 2. REGISTRO DE EVENTOS (IPC)
// -----------------------------------------------------------------------------
registerHandlers();

// -----------------------------------------------------------------------------
// 3. ARRANQUE DE LA INTERFAZ
// -----------------------------------------------------------------------------
app.whenReady().then(() => {
    const lastConfig = configManager.loadLastConfig();
    
    if (lastConfig && lastConfig.size) {
        logManager.log('INFO', 'INIT', `Restaurando sesión previa.`); 
        
        process.nextTick(() => {
            ipcMain.emit('selection-made', null, lastConfig); 
        });
    } else {
        logManager.log('INFO', 'INIT', 'Abriendo Selector.'); 
        windowManager.createSelectorWindow();
    }
});

// -----------------------------------------------------------------------------
// 4. CIERRE
// -----------------------------------------------------------------------------
app.on('window-all-closed', () => { 
    if (process.platform !== 'darwin') app.quit(); 
    logManager.log('INFO', 'APP_QUIT', 'Aplicación terminada.'); 
});