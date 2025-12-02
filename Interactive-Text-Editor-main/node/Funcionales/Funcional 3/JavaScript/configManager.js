// JavaScript/configManager.js

const fs = require('fs');
const path = require('path');
const LAST_CONFIG_KEY = 'lastConfiguration';

let config;
let configPath; // Aquí se guarda la ruta activa (debería ser .../resources/InteractiveContentDisplay.json)

// Carga la configuración inicial desde el disco
function loadConfig(filePath) {
    const logManager = require('./logManager'); 
    
    configPath = filePath; 
    console.log(`[CONFIG MANAGER] Ruta de configuración establecida en: ${configPath}`);

    try {
        const configData = fs.readFileSync(configPath, 'utf-8');
        config = JSON.parse(configData);
        return config;
    } catch (error) {
        console.error('[CONFIG FATAL ERROR] Error en loadConfig:', error);
        if (logManager && logManager.logError) logManager.logError('CONFIG_LOAD', error); 
        throw error; 
    }
}

// Guarda la última selección del usuario
function saveLastConfig(data) {
    const logManager = require('./logManager');
    
    // VALIDACIÓN: Si no hay ruta definida, no podemos guardar
    if (!configPath) {
        const msg = '[CONFIG ERROR] Intentando guardar sin ruta definida (loadConfig no se ejecutó correctamente).';
        console.error(msg);
        if (logManager) logManager.logError('CONFIG_SAVE_NO_PATH', msg);
        return;
    }

    try {
        console.log(`[CONFIG] Intentando guardar configuración en: ${configPath}`);

        // Leemos de nuevo para asegurar que no sobrescribimos cambios externos
        const currentConfigData = fs.readFileSync(configPath, 'utf-8');
        let currentConfig = JSON.parse(currentConfigData);
        
        // Actualizamos solo la llave de lastConfig
        currentConfig[LAST_CONFIG_KEY] = data;
        
        // Escribimos al disco
        fs.writeFileSync(configPath, JSON.stringify(currentConfig, null, 2), 'utf-8');
        
        console.log('[CONFIG] ✓ ÉXITO: Archivo actualizado correctamente.');
        logManager.log('INFO', 'CONFIG_SAVED', `Configuración guardada en ${configPath}`);

    } catch (error) {
        console.error('[CONFIG ERROR] Fallo al escribir en disco:', error);
        logManager.logError('CONFIG_SAVE_WRITE', error); 
    }
}

// Recupera la configuración guardada anteriormente
function loadLastConfig() {
    if (config && config[LAST_CONFIG_KEY]) {
        return config[LAST_CONFIG_KEY];
    }
    return null;
}

function getConfig() {
    return config;
}

module.exports = {
    loadConfig,
    saveLastConfig,
    loadLastConfig,
    getConfig,
    LAST_CONFIG_KEY
};