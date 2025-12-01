// JavaScript/pathManager.js

const path = require('path');
const url = require('url');
const { getConfig } = require('./configManager');
const logManager = require('./logManager'); 

// --- FUNCIÓN CLAVE ---
// Recupera la ruta base que calculamos en main.js
const getBasePath = () => {
    // Si existe la global (producción/ejecución normal), úsala.
    // Si no (tests unitarios aislados), usa fallback relativo.
    return global.APP_BASE_PATH || path.join(__dirname, '..');
};

const appRoot = path.join(__dirname, '..'); 
const preloadScript = path.join(__dirname, 'preload.js'); 

function getFileUrl(filePath) {
    return url.pathToFileURL(path.normalize(filePath)).href;
}

module.exports = {
    appRoot,
    preloadScript,
    getFileUrl,

    // --- Rutas dinámicas (Leen desde config y son relativas al EXE) ---
    get resourcesDir() {
        try {
            const config = getConfig();
            if (!config) throw new Error("Config not loaded");
            
            // AQUÍ ESTÁ EL CAMBIO: 
            // Une la carpeta del .exe con el nombre de la carpeta de recursos (ej: "media_content")
            return path.join(getBasePath(), config.resourcesDir);
        } catch (error) {
            logManager.logFatal('PATH_RESOURCES_DIR', error);
            throw error;
        }
    },
    
    // --- El resto de getters usan 'this.resourcesDir', así que funcionarán automáticamente ---

    get htmlDir() {
        try {
            const config = getConfig();
            return path.join(appRoot, config.htmlDirName);
        } catch (error) {
            logManager.logFatal('PATH_HTML_DIR', error);
            throw error;
        }
    },

    get imagesDir() {
        try {
            const config = getConfig();
            return path.join(this.resourcesDir, config.imageDirName);
        } catch (error) {
            logManager.logFatal('PATH_IMAGES_DIR', error);
            throw error;
        }
    },

    get userFile() {
        try {
            const config = getConfig();
            return path.join(this.resourcesDir, config.userFileName);
        } catch (error) {
            logManager.logFatal('PATH_USER_FILE', error);
            throw error;
        }
    },
    
    get bannersTopPath() {
        try {
            const config = getConfig();
            return path.join(this.imagesDir, config.bannersTopDirName);
        } catch (error) {
            logManager.logFatal('PATH_BANNERS_TOP', error);
            throw error;
        }
    },
    
    get bannersBottomPath() {
        try {
            const config = getConfig();
            return path.join(this.imagesDir, config.bannersBottomDirName);
        } catch (error) {
            logManager.logFatal('PATH_BANNERS_BOTTOM', error);
            throw error;
        }
    },

    get mobileImgsPath() {
        try {
            const config = getConfig();
            return path.join(this.imagesDir, config.mobileImgsDirName);
        } catch (error) {
            logManager.logFatal('PATH_MOBILE_IMGS', error);
            throw error;
        }
    },
    
    get logFilePath() {
        try {
            const config = getConfig();
            return config.logFilePath; 
        } catch (error) {
            console.error("[FATAL] Fallo al obtener logFilePath:", error);
            throw error;
        }
    },

    // --- Rutas HTML ---
    get selectorHtml() { return path.join(this.htmlDir, 'selector.html'); },
    get indexHtml() { return path.join(this.htmlDir, 'index.html'); },
    get backgroundHtml() { return path.join(this.htmlDir, 'background.html'); },

    // --- Icono ---
    get iconPath() {
        try {
            const config = getConfig();
            return path.join(this.resourcesDir, config.iconPath); 
        } catch (error) {
            console.error(error);
            logManager.logFatal('PATH_ICON', error);
            throw error;
        }
    }
};