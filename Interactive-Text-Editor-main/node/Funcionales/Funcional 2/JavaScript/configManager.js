// JavaScript/configManager.js

const fs = require('fs');
const LAST_CONFIG_KEY = 'lastConfiguration';

// NOTA: logManager se importa DENTRO de las funciones para evitar dependencias circulares,
// ya que logManager podría necesitar configManager en algún punto futuro.

let config;
let configPath;

// Carga la configuración inicial desde el disco
function loadConfig(filePath) {
    const logManager = require('./logManager'); 
    
    configPath = filePath; 
    try {
        const configData = fs.readFileSync(configPath, 'utf-8');
        config = JSON.parse(configData);
        return config;
    } catch (error) {
        console.error('[CONFIG FATAL ERROR] Error en loadConfig:', error);
        // Si falla aquí, logManager puede no estar inicializado, pero intentamos
        if (logManager && logManager.logError) logManager.logError('CONFIG_LOAD', error); 
        throw error; // El error debe subir a main.js para detener la app
    }
}

// Guarda la última selección del usuario (tamaño, archivos) en el JSON
function saveLastConfig(data) {
    const logManager = require('./logManager');
    
    try {
        // Leemos de nuevo para asegurar que tenemos la versión más reciente
        const currentConfigData = fs.readFileSync(configPath, 'utf-8');
        let currentConfig = JSON.parse(currentConfigData);
        
        // Actualizamos solo la llave de lastConfig
        currentConfig[LAST_CONFIG_KEY] = data;
        
        // Escribimos al disco
        fs.writeFileSync(configPath, JSON.stringify(currentConfig, null, 2), 'utf-8');
        console.log('[CONFIG] Ultima configuración guardada con exito.');
    } catch (error) {
        console.error('[CONFIG ERROR] No se pudo guardar la ultima configuración:', error);
        logManager.logError('CONFIG_SAVE', error); 
    }
}

// Recupera la configuración guardada anteriormente (si existe)
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