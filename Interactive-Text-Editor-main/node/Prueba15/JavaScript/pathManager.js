const path = require('path');
const url = require('url');
const { getConfig, init: initConfig } = require('./configManager'); 
const { app } = require('electron'); 

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
        const baseDir = this.resourcesDir; 
        const config = getConfig();
        
        if (!config.imageDirName) {
            console.error('[PATH ERROR] imageDirName no está definido. Revisar configManager.js y config.json.');
            throw new Error('imagesDir: Configuración de ruta de imagen incompleta (imageDirName).');
        }
        
        return path.join(baseDir, config.imageDirName);
    },

    // 3. RUTA HTML (CORRECCIÓN FINAL Y MÁS ROBUSTA para ASAR)
    get htmlDir() {
        // Si está empaquetado, usamos app.getAppPath() que apunta a la raíz del ASAR.
        if (app.isPackaged) {
            return path.join(app.getAppPath(), 'html');
        }
        // En desarrollo, usamos la ruta relativa tradicional.
        return path.join(__dirname, '..', 'html'); 
    },

    // --- Otras Rutas (Usan imagesDir o resourcesDir) ---
    get userFile() {
        const config = getConfig();
        if (!config) throw new Error("Config not loaded before accessing 'userFile'");
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