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
    const resourcePath = config.resourcesDir;
    
    // VERIFICACIÓN CLAVE: Si la ruta empieza con una unidad de disco (C:, D:, etc.)
    // O si es una ruta absoluta de Unix/Linux, ÚSALA DIRECTAMENTE.
    if (path.isAbsolute(resourcePath) || /^[a-zA-Z]:/.test(resourcePath)) {
        return resourcePath; // Retorna C:\estacio directamente
    }
    
    // Si no es absoluta, usa la lógica anterior (relativa a DATA_DIR)
    return path.join(global.DATA_DIR, resourcePath);
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
        const absolutePath = config.userFilePathAbsolute; // Lee la nueva ruta
        
        // 1. Verificar si se configuró una ruta absoluta
        if (absolutePath && path.isAbsolute(absolutePath)) {
            // Si es una ruta absoluta, se usa directamente (c:\estacio\display.txt)
            return absolutePath;
        }

        // 2. Si no es absoluta, usa la lógica anterior (relativa a resourcesDir)
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