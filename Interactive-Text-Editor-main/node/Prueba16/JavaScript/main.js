// JavaScript/main.js

const { app, ipcMain } = require('electron');
const path = require('path');
const configManager = require('./configManager');
const windowManager = require('./windowManager');
const { registerHandlers } = require('./ipcHandlers');

// 1. Cargar configuración
// Usamos path.join(__dirname, '..', ...) porque __dirname ahora es la carpeta 'JavaScript'
try {
    const configPath = path.join(__dirname, '..', 'config', 'config.json');
    configManager.loadConfig(configPath);
    console.log('[CONFIG] Archivo de configuración cargado con éxito.');
} catch (error) {
    console.error('[CONFIG FATAL ERROR] No se pudo cargar o parsear config.json. ¡La aplicación no puede continuar!', error);
    app.quit();
    return; // Salir del script si la config falla
}

// 2. Registrar todos los manejadores IPC
registerHandlers();

// 3. Iniciar la aplicación
app.whenReady().then(() => {
    const lastConfig = configManager.loadLastConfig();
    
    if (lastConfig && lastConfig.size) {
        console.log('[INIT] Ultima configuración encontrada, recargando...');
        // Usar nextTick para asegurar que los listeners IPC (en ipcHandlers) estén listos
        process.nextTick(() => {
            // Emitir el evento que 'ipcHandlers' está escuchando
            ipcMain.emit('selection-made', null, lastConfig); 
        });
    } else {
        console.log('[INIT] No se encontró última configuración, abriendo selector.');
        windowManager.createSelectorWindow();
    }
});

// 4. Manejar cierre
app.on('window-all-closed', () => { 
    if (process.platform !== 'darwin') app.quit(); 
});