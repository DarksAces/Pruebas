// JavaScript/pathManager.js

const path = require('path');
const url = require('url');
const { getConfig } = require('./configManager');

// --- Rutas que NO dependen de config ---
const appRoot = path.join(__dirname, '..'); // Sube un nivel desde /JavaScript
const preloadScript = path.join(__dirname, 'preload.js'); 

// Helper para URLs
function getFileUrl(filePath) {
    return url.pathToFileURL(path.normalize(filePath)).href;
}

// --- Exportamos las rutas ---
// Usamos "getters" para que el valor de 'config' se obtenga
// EN EL MOMENTO en que se pide la ruta, no al cargar el archivo.

module.exports = {
    // --- Rutas estaticas ---
    appRoot,
    preloadScript,
    getFileUrl,

    // --- Rutas dinamicas (dependen de config) ---
    get resourcesDir() {
        const config = getConfig();
        if (!config) throw new Error("Config not loaded before accessing 'resourcesDir'");
        return path.resolve(config.resourcesDir);
    },
    
    get htmlDir() {
        const config = getConfig();
        if (!config) throw new Error("Config not loaded before accessing 'htmlDir'");
        return path.join(appRoot, config.htmlDirName);
    },

    get imagesDir() {
        const config = getConfig();
        if (!config) throw new Error("Config not loaded before accessing 'imagesDir'");
        return path.join(this.resourcesDir, config.imageDirName);
    },

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