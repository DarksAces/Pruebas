// JavaScript/pathManager.js

const path = require('path');
const url = require('url');
const { getConfig } = require('./configManager');
// Importación añadida para logging
const logManager = require('./logManager'); 

// --- Rutas que NO dependen de config ---
const appRoot = path.join(__dirname, '..'); // Sube un nivel desde /JavaScript
const preloadScript = path.join(__dirname, 'preload.js'); 

// Helper para URLs
function getFileUrl(filePath) {
    return url.pathToFileURL(path.normalize(filePath)).href;
}

// --- Exportamos las rutas ---
module.exports = {
    // --- Rutas estáticas ---
    appRoot,
    preloadScript,
    getFileUrl,

    // --- Rutas dinámicas (dependen de config) ---
    get resourcesDir() {
        try {
            const config = getConfig();
            if (!config) throw new Error("Config not loaded before accessing 'resourcesDir'");
            return path.resolve(config.resourcesDir);
        } catch (error) {
            logManager.logFatal('PATH_RESOURCES_DIR', error);
            throw error;
        }
    },
    
    get htmlDir() {
        try {
            const config = getConfig();
            if (!config) throw new Error("Config not loaded before accessing 'htmlDir'");
            return path.join(appRoot, config.htmlDirName);
        } catch (error) {
            logManager.logFatal('PATH_HTML_DIR', error);
            throw error;
        }
    },

    get imagesDir() {
        try {
            const config = getConfig();
            if (!config) throw new Error("Config not loaded before accessing 'imagesDir'");
            return path.join(this.resourcesDir, config.imageDirName);
        } catch (error) {
            logManager.logFatal('PATH_IMAGES_DIR', error);
            throw error;
        }
    },

    get userFile() {
        try {
            const config = getConfig();
            if (!config) throw new Error("Config not loaded before accessing 'userFile'");
            return path.join(this.resourcesDir, config.userFileName);
        } catch (error) {
            logManager.logFatal('PATH_USER_FILE', error);
            throw error;
        }
    },
    

    get bannersTopPath() {
        try {
            const config = getConfig();
            if (!config) throw new Error("Config not loaded before accessing 'bannersTopPath'");
            return path.join(this.imagesDir, config.bannersTopDirName);
        } catch (error) {
            logManager.logFatal('PATH_BANNERS_TOP', error);
            throw error;
        }
    },
    
    get bannersBottomPath() {
        try {
            const config = getConfig();
            if (!config) throw new Error("Config not loaded before accessing 'bannersBottomPath'");
            return path.join(this.imagesDir, config.bannersBottomDirName);
        } catch (error) {
            logManager.logFatal('PATH_BANNERS_BOTTOM', error);
            throw error;
        }
    },

    get mobileImgsPath() {
        try {
            const config = getConfig();
            if (!config) throw new Error("Config not loaded before accessing 'mobileImgsPath'");
            return path.join(this.imagesDir, config.mobileImgsDirName);
        } catch (error) {
            logManager.logFatal('PATH_MOBILE_IMGS', error);
            throw error;
        }
    },
    
    get logFilePath() {
        try {
            const config = getConfig();
            if (!config) throw new Error("Config not loaded before accessing 'logFilePath'");
            return config.logFilePath; 
        } catch (error) {
            console.error("[FATAL] Fallo al obtener logFilePath:", error);
            throw error;
        }
    },

    // --- Rutas HTML (dependen de htmlDir) ---
    get selectorHtml() {
        try {
            return path.join(this.htmlDir, 'selector.html');
        } catch (error) {
            logManager.logFatal('PATH_SELECTOR_HTML', error);
            throw error;
        }
    },
    
    get indexHtml() {
        try {
            return path.join(this.htmlDir, 'index.html');
        } catch (error) {
            logManager.logFatal('PATH_INDEX_HTML', error);
            throw error;
        }
    },

    get backgroundHtml() {
        try {
            return path.join(this.htmlDir, 'background.html');
        } catch (error) {
            logManager.logFatal('PATH_BACKGROUND_HTML', error);
            throw error;
        }
    },

    // --- NUEVO: RUTA AL ICONO ---
    get iconPath() {
        try {
            const config = getConfig();
            if (!config) throw new Error("Config not loaded before accessing 'iconPath'");
            // Une 'C:\recursos' con 'imagenes/icon/icon.png'
            return path.join(this.resourcesDir, config.iconPath); 
        } catch (error) {
            // Usamos console error directo por si el logManager falla, pero intentamos loguear
            console.error("[FATAL] Fallo al obtener iconPath:", error);
            logManager.logFatal('PATH_ICON', error);
            throw error;
        }
    }
};