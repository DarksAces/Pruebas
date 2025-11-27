// JavaScript/configManager.js

const fs = require('fs');
const LAST_CONFIG_KEY = 'lastConfiguration';

// La importación de logManager ha sido ELIMINADA de aquí
// para evitar dependencias circulares.

let config;
let configPath;

function loadConfig(filePath) {
    // Importación movida AQUI
    const logManager = require('./logManager'); 
    
    configPath = filePath;
    try {
        const configData = fs.readFileSync(configPath, 'utf-8');
        config = JSON.parse(configData);
        return config;
    } catch (error) {
        console.error('[CONFIG FATAL ERROR] Error en loadConfig:', error);
        logManager.logError('CONFIG_LOAD', error); 
        throw error; // Relanzar para que main.js lo atrape
    }
}

function saveLastConfig(data) {
    // Importación movida AQUI
    const logManager = require('./logManager');
    
    try {
        const currentConfigData = fs.readFileSync(configPath, 'utf-8');
        let currentConfig = JSON.parse(currentConfigData);
        currentConfig[LAST_CONFIG_KEY] = data;
        fs.writeFileSync(configPath, JSON.stringify(currentConfig, null, 2), 'utf-8');
        console.log('[CONFIG] Ultima configuración guardada con exito.');
    } catch (error) {
        console.error('[CONFIG ERROR] No se pudo guardar la ultima configuración:', error);
        logManager.logError('CONFIG_SAVE', error); 
    }
}

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