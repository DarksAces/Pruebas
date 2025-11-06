const { app } = require('electron');
const path = require('path');
const fs = require('fs');

const LAST_CONFIG_KEY = 'lastConfiguration';
// Define aquí la estructura de configuración por defecto para evitar fallos
const DEFAULT_CONFIG = {
    // CAMBIO CLAVE: Usamos la ruta absoluta C:\resources en desarrollo
    resourcesDir: process.env.NODE_ENV === 'development' 
        ? 'C:\\resources' 
        : path.join(__dirname, '..', 'resources'), // Esta es la ruta por defecto para cuando está empaquetada (dentro de .asar)
    iconPath: 'assets/icon.png', // Fallback para el icono
    apiEndpoint: 'http://localhost:8080/dev', 
    // Añade otras configuraciones por defecto aquí
}; 

let config;
let configPath;

/**
 * 1. Define la ubicación del archivo config.json (Editable)
 */
function getConfigPath() {
    if (app.isPackaged) {
        return path.join(process.resourcesPath, 'config', 'config.json');
    }
    // En desarrollo:
    return path.join(__dirname, '..', 'config', 'config.json');
}


/**
 * 2. Carga la configuración, priorizando el archivo editable, o usando por defecto.
 * ESTA ES LA FUNCIÓN DE INICIALIZACIÓN PRINCIPAL.
 * NO ACEPTA PARÁMETROS.
 * @returns {object} La configuración final cargada.
 */
function init() {
    configPath = getConfigPath();
    let loadedConfig = DEFAULT_CONFIG;

    console.log(`[CONFIG] Intentando cargar config editable desde: ${configPath}`);

    try {
        if (fs.existsSync(configPath)) {
            const configData = fs.readFileSync(configPath, 'utf-8');
            const userConfig = JSON.parse(configData);
            
            // Fusionar: Valores por defecto + Valores del usuario
            loadedConfig = { ...DEFAULT_CONFIG, ...userConfig };
            
            // Si el config.json editable tiene una ruta resourcesDir, la usa
            if (userConfig.resourcesDir) {
                loadedConfig.resourcesDir = userConfig.resourcesDir;
            }
            
            console.log('[CONFIG] Configuración editable cargada con éxito.');
        } else {
            console.warn('[CONFIG WARNING] Archivo config.json editable no encontrado. Usando valores por defecto.');
        }
    } catch (error) {
        console.error('[CONFIG FATAL ERROR] Falló la carga del archivo editable. Usando valores por defecto.', error.message);
        // NO HACEMOS THROW, solo retornamos el default para evitar que la app.quit() se active
    }
    
    config = loadedConfig;
    return config;
}

// --- Tu lógica existente, adaptada a la nueva estructura ---

function saveLastConfig(data) {
    if (!config || !configPath) {
        console.error('[CONFIG ERROR] No se puede guardar: La configuración inicial nunca fue cargada.');
        return;
    }
    
    try {
        // Leemos el archivo actual para no sobrescribir otras configuraciones
        const currentConfigData = fs.readFileSync(configPath, 'utf-8');
        let currentConfig = JSON.parse(currentConfigData);
        
        currentConfig[LAST_CONFIG_KEY] = data;
        
        fs.writeFileSync(configPath, JSON.stringify(currentConfig, null, 2), 'utf-8');
        
        // Actualizar la variable global 'config' en memoria
        config[LAST_CONFIG_KEY] = data; 
        
        console.log('[CONFIG] Ultima configuracion guardada con exito.');
    } catch (error) {
        console.error('[CONFIG ERROR] No se pudo guardar la ultima configuracion:', error.message);
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
    init, // Usamos 'init' en lugar de 'loadConfig'
    saveLastConfig,
    loadLastConfig,
    getConfig,
    LAST_CONFIG_KEY
};