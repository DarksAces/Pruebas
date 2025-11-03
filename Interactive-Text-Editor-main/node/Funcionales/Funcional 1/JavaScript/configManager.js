// JavaScript/configManager.js

/*
 * Módulo encargado de leer/escribir la configuración global del proyecto
 * - loadConfig(path): carga y parsea `config.json` y lo deja disponible via getConfig()
 * - saveLastConfig(data): escribe en el campo LAST_CONFIG_KEY dentro de config.json
 * - loadLastConfig(): retorna la última configuración guardada (o null)
 *
 * Contratos y comportamientos importantes:
 *  - loadConfig debe invocarse al inicio (main.js) antes de acceder a getters en otros módulos.
 *  - Si loadConfig falla, se relanza el error (main.js debe manejar y terminar si es crítico).
 *  - saveLastConfig hace una lectura-modificación-escritura sencilla; no es transaccional.
 */

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
        // Relanzamos para que el proceso que llama (normalmente main.js) decida qué hacer
        throw error;
    }
}

function saveLastConfig(data) {
    try {
        const currentConfigData = fs.readFileSync(configPath, 'utf-8');
        let currentConfig = JSON.parse(currentConfigData);
        currentConfig[LAST_CONFIG_KEY] = data;
        fs.writeFileSync(configPath, JSON.stringify(currentConfig, null, 2), 'utf-8');
        console.log('[CONFIG] Ultima configuración guardada con exito.');
    } catch (error) {
        console.error('[CONFIG ERROR] No se pudo guardar la ultima configuración:', error);
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