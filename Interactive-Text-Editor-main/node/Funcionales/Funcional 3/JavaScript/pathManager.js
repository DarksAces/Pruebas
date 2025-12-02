// JavaScript/pathManager.js
// ============================================================================
// GESTOR DE RUTAS - TODO DESDE APPDATA
// ============================================================================

const path = require('path');
const url = require('url');
const { getConfig } = require('./configManager');
const logManager = require('./logManager'); 

// Constantes
const appRoot = path.join(__dirname, '..'); 
const preloadScript = path.join(__dirname, 'preload.js'); 

function getFileUrl(filePath) {
    return url.pathToFileURL(path.normalize(filePath)).href;
}

module.exports = {
    appRoot,
    preloadScript,
    getFileUrl,

    // ========================================================================
    // RUTAS DESDE LA CARPETA DE INSTALACIÓN (global.DATA_DIR)
    // ========================================================================
    get resourcesDir() {
        const config = getConfig();
        return path.join(global.DATA_DIR, config.resourcesDir);
    },

    get htmlDir() {
        const config = getConfig();
        return path.join(appRoot, config.htmlDirName);
    },

    get imagesDir() {
        const config = getConfig();
        return path.join(this.resourcesDir, config.imageDirName);
    },

    get userFile() {
        const config = getConfig();
        return path.join(this.resourcesDir, config.userFileName);
    },
    
    get bannersTopPath() {
        const config = getConfig();
        return path.join(this.imagesDir, config.bannersTopDirName);
    },
    
    get bannersBottomPath() {
        const config = getConfig();
        return path.join(this.imagesDir, config.bannersBottomDirName);
    },

    get mobileImgsPath() {
        const config = getConfig();
        return path.join(this.imagesDir, config.mobileImgsDirName);
    },
    
    get logFilePath() {
        const config = getConfig();
        return config.logFilePath;
    },

    get selectorHtml() { return path.join(this.htmlDir, 'selector.html'); },
    get indexHtml() { return path.join(this.htmlDir, 'index.html'); },
    get backgroundHtml() { return path.join(this.htmlDir, 'background.html'); },

    get iconPath() {
        const config = getConfig();
        return path.join(this.resourcesDir, config.iconPath);
    }
};