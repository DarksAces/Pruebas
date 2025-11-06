// JavaScript/windowManager.js
const { app, BrowserWindow } = require('electron');
const path = require('path');
const fs = require('fs');
const appState = require('./appState');
const pathManager = require('./pathManager');
const { clearInactivityTimer } = require('./inactivityManager');
const configManager = require('./configManager');

const configPath = path.join(__dirname, '..', 'config', 'config.json');

/**
 * Resuelve la ruta absoluta del icono de la aplicacion.
 */
function getIconFullPath() {
    const config = configManager.getConfig();
    if (config.resourcesDir && config.iconPath) {
        // Aseguramos que usamos la misma logica para todas las ventanas
        return path.join(config.resourcesDir, config.iconPath);
    }
    return undefined;
}

/**
 * Guarda los limites de la ventana principal en el archivo config.json real.
 */
function saveWindowBounds(window) {
  if (!window || window.isDestroyed()) return;

const bounds = window.getBounds();

    try {
     // Aseguramos que la carpeta de configuracion existe
    const configDir = path.dirname(configPath);
    if (!fs.existsSync(configDir)) fs.mkdirSync(configDir, { recursive: true });

    const raw = fs.existsSync(configPath) ? fs.readFileSync(configPath, 'utf8') : '{}';
    const config = JSON.parse(raw);

    if (!config.lastConfiguration) config.lastConfiguration = {};
    config.lastConfiguration.windowBounds = {
      x: bounds.x,
      y: bounds.y,
      width: bounds.width,
      height: bounds.height,
    };

    fs.writeFileSync(configPath, JSON.stringify(config, null, 2));
    console.log('[CONFIG] Posicion guardada en config.json:', config.lastConfiguration.windowBounds);
  } catch (err) {
    console.error('[CONFIG ERROR] No se pudo guardar posicion:', err);
 }
}

/**
 * Activa el seguimiento de movimiento y tamano de la ventana.
 */
function watchWindowPosition(window) {
  const save = () => saveWindowBounds(window);
  window.on('move', save);
  window.on('resize', save);
  window.on('close', save);
}

/**
 * Crea la ventana de seleccion inicial.
 */
function createSelectorWindow() {
  if (appState.winSelector) return;

  const config = configManager.getConfig();
  const iconFullPath = getIconFullPath(); // Usamos la nueva funcion

  const win = new BrowserWindow({
    width: 450,
    height: 650,
    frame: true,
    resizable: false,
    icon: iconFullPath, // Icono aplicado aqui
    webPreferences: {
    preload: pathManager.preloadScript,
    contextIsolation: true,
    nodeIntegration: false,
  },
  });

  win.setMenu(null);
  // CAMBIO CLAVE 1: Aseguramos la ruta URL para el archivo HTML
  win.loadURL(pathManager.getFileUrl(pathManager.selectorHtml));

  win.on('closed', () => {
    appState.winSelector = null;
    if (!appState.windows.length) app.quit();
  });

  appState.winSelector = win;
}

/**
 * Crea una ventana (principal o fondo).
 */
function createWindow(bounds, isMain = false) {
  const config = configManager.getConfig();
  const lastBounds = config?.lastConfiguration?.windowBounds;
  const iconFullPath = getIconFullPath(); // OBTENEMOS EL ICONO AQUÍ

   // Restaurar posicion previa si existe
  if (isMain && lastBounds) {
    bounds.x = lastBounds.x ?? bounds.x;
    bounds.y = lastBounds.y ?? lastBounds.y;
    bounds.width = lastBounds.width ?? bounds.width;
    bounds.height = lastBounds.height ?? bounds.height;
    console.log('[CONFIG] Restaurando posicion previa:', lastBounds);
}

  console.log(`[VENTANA] Creando ventana ${isMain ? 'PRINCIPAL' : 'FONDO'} en:`, bounds);

  const isTransparent = !isMain;

  const win = new BrowserWindow({
    x: bounds.x,
    y: bounds.y,
    width: bounds.width,
    height: bounds.height,
    frame: false,
    transparent: isTransparent,
    resizable: false,
    alwaysOnTop: true,
    focusable: isMain,
    skipTaskbar: !isMain,
    backgroundColor: '#000000',
    hasShadow: false,
    icon: iconFullPath, // ICONO APLICADO A LA VENTANA PRINCIPAL/FONDO
    webPreferences: {
      preload: pathManager.preloadScript,
      contextIsolation: true,
      webSecurity: false,
    },
});

  win.setAlwaysOnTop(true, 'screen-saver');

  if (isMain) {
    // CAMBIO CLAVE 2: Aseguramos la ruta URL para el archivo HTML
    win.loadURL(pathManager.getFileUrl(pathManager.indexHtml));
    win.setIgnoreMouseEvents(false);

    // Atajo Ctrl+Shift+R → volver al selector
    win.webContents.on('before-input-event', (event, input) => {
    if (input.control && input.shift && input.key.toLowerCase() === 'r') {
        console.log('[ATAJO] Ctrl+Shift+R detectado - Volviendo al selector');
        event.preventDefault();
        closeAllWindows();
        clearInactivityTimer();
        createSelectorWindow();
    }
    });

    // Guardar posicion automaticamente
    watchWindowPosition(win);

  } else {
    // CAMBIO CLAVE 3: Aseguramos la ruta URL para el archivo HTML
    win.loadURL(pathManager.getFileUrl(pathManager.backgroundHtml));
    win.setIgnoreMouseEvents(true);
}

  if (bounds.index !== undefined) win.positionIndex = bounds.index;

  appState.windows.push(win);
  return win;
}

/**
 * Cierra todas las ventanas abiertas.
 */
function closeAllWindows() {
  appState.windows.forEach((w) => {
    if (!w.isDestroyed()) w.close();
  });
  appState.windows = [];
}

/**
 * Exportar para acceder a la ventana principal desde main.js para el manejo de cierre
 */
function getMainWindow() {
    // Asume que la ventana principal es la primera en el array o tiene una referencia
    return appState.windows.find(w => w.positionIndex === 0) || appState.windows[0]; 
}

module.exports = {
  createSelectorWindow,
  createWindow,
  closeAllWindows,
  getMainWindow, // Exportamos para que main.js pueda usarla en registerCloseHandler
};