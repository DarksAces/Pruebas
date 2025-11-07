// JavaScript/configManager.js

const fs = require('fs');
const LAST_CONFIG_KEY = 'lastConfiguration';

let config;
let configPath;

function loadConfig(filePath) {
    configPath = filePath;
    try {
        const configData = fs.readFileSync(configPath, 'utf-8');
        config = JSON.parse(configData);
        return config;
    } catch (error) {
        console.error('[CONFIG FATAL ERROR] Error en loadConfig:', error);
        throw error; // Relanzar para que main.js lo atrape
    }
}

function saveLastConfig(data) {
    try {
        const currentConfigData = fs.readFileSync(configPath, 'utf-8');
        let currentConfig = JSON.parse(currentConfigData);
        currentConfig[LAST_CONFIG_KEY] = data;
        fs.writeFileSync(configPath, JSON.stringify(currentConfig, null, 2), 'utf-8');
        console.log('[CONFIG] Ultima configuracion guardada con exito.');
    } catch (error) {
        console.error('[CONFIG ERROR] No se pudo guardar la ultima configuracion:', error);
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