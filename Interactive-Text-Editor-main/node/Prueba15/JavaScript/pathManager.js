// JavaScript/pathManager.js

const path = require('path');
const url = require('url');
const { getConfig, init: initConfig } = require('./configManager'); 

// --- CRÍTICO: Forzar la inicialización al cargar el módulo ---
// Esto asegura que getConfig() devuelva valores por defecto si main.js no ha corrido init() aún.
initConfig(); 

// --- Rutas que NO dependen de config ---
const appRoot = path.join(__dirname, '..'); // Sube un nivel desde /JavaScript
const preloadScript = path.join(__dirname, 'preload.js'); 

// Helper para URLs
function getFileUrl(filePath) {
    // Usar la función de URL de Node para la máxima compatibilidad ASAR
    return url.pathToFileURL(path.normalize(filePath)).href;
}

// --- Exportamos las rutas ---
module.exports = {
    appRoot,
    preloadScript,
    getFileUrl,

    // 1. RUTA BASE: Garantiza que el valor es resuelto y es una cadena.
    get resourcesDir() {
        const config = getConfig();
        if (!config || !config.resourcesDir) {
             throw new Error("Configuración de resourcesDir ausente o fallida.");
        }
        return path.resolve(config.resourcesDir);
    },
    
    // 2. RUTA IMÁGENES: Depende de resourcesDir y valida el valor de la configuración.
    get imagesDir() {
        // Llama al getter resourcesDir, forzando su validación y obteniendo la base (ej. C:\recursos)
        const baseDir = this.resourcesDir; 
        const config = getConfig();
        
        if (!config.imageDirName) {
            console.error('[PATH ERROR] imageDirName no está definido. Revisar configManager.js y config.json.');
            // El error ocurría aquí; ahora lanzamos un error claro en lugar de devolver undefined
            throw new Error('imagesDir: Configuración de ruta de imagen incompleta (imageDirName).');
        }
        
        return path.join(baseDir, config.imageDirName);
    },

    // 3. RUTA HTML (Corrige problemas de ASAR): Construir la ruta HTML directamente.
    get htmlDir() {
        // Asumiendo que pathManager.js está en /JavaScript y html/ está en la raíz del ASAR.
        return path.join(__dirname, '..', 'html'); 
    },

    // --- Otras Rutas (Usan imagesDir o resourcesDir) ---
    get userFile() {
        const config = getConfig();
        if (!config) throw new Error("Config not loaded before accessing 'userFile'");
        // Ya que userFileName es un nombre de archivo, solo depende de resourcesDir
        return path.join(this.resourcesDir, config.userFileName);
    },
    
    get welcomeImage() {
        const config = getConfig();
        if (!config) throw new Error("Config not loaded before accessing 'welcomeImage'");
        return path.join(this.imagesDir, config.defaultWelcomeImagePath);
    },
    
    get bannersTopPath() {
        const config = getConfig();
        if (!config) throw new Error("Config not loaded before accessing 'bannersTopPath'");
        // Llama a imagesDir, que ya es un path garantizado
        return path.join(this.imagesDir, config.bannersTopDirName);
    },
    
    get bannersBottomPath() {
        const config = getConfig();
        if (!config) throw new Error("Config not loaded before accessing 'bannersBottomPath'");
        return path.join(this.imagesDir, config.bannersBottomDirName);
    },

    get mobileImgsPath() {
        const config = getConfig();
        if (!config) throw new Error("Config not loaded before accessing 'mobileImgsPath'");
        return path.join(this.imagesDir, config.mobileImgsDirName);
    },

    // --- Rutas HTML (dependen de htmlDir) ---
    get selectorHtml() {
        return path.join(this.htmlDir, 'selector.html');
    },
    
    get indexHtml() {
        return path.join(this.htmlDir, 'index.html');
    },

    get backgroundHtml() {
        return path.join(this.htmlDir, 'background.html');
    }
};