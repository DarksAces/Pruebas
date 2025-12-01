// JavaScript/pathManager.js

const path = require('path');
const url = require('url');
const { getConfig } = require('./configManager');
const logManager = require('./logManager'); 

// --- Rutas estáticas (relativas a la estructura del proyecto) ---
const appRoot = path.join(__dirname, '..'); 
const preloadScript = path.join(__dirname, 'preload.js'); 

// Helper: Convierte ruta de archivo (C:\...) a URL (file://...) para Electron
function getFileUrl(filePath) {
    return url.pathToFileURL(path.normalize(filePath)).href;
}

// --- Exportamos las rutas ---
// Usamos 'get' para evaluar la ruta en el momento del acceso, no al inicio.
module.exports = {
    appRoot,
    preloadScript,
    getFileUrl,

    // --- Rutas dinámicas (Leen desde configManager) ---
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
    
    // Directorios de imágenes específicas
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

    // --- Rutas HTML ---
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
    }
};