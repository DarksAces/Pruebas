// JavaScript/windowManager.js
const { app, BrowserWindow, screen } = require('electron'); 
const path = require('path');
const fs = require('fs');
const appState = require('./appState');
const pathManager = require('./pathManager');
const { clearInactivityTimer } = require('./inactivityManager');
const configManager = require('./configManager');

const configPath = path.join(__dirname, '..', 'config', 'config.json');

// --- LÓGICA DE GESTIÓN DE DISPLAYS ---
let primaryDisplay; 
let secondaryDisplay; 

function initializeDisplays() {
    const displays = screen.getAllDisplays();
    const systemPrimary = screen.getPrimaryDisplay(); 
    const systemSecondary = displays.find(d => d.id !== systemPrimary.id);

    // INVERSIÓN: La ventana principal (APP) va al monitor secundario (FÍSICO).
    if (systemSecondary) {
        primaryDisplay = systemSecondary; 
        secondaryDisplay = systemPrimary; 
        console.log('[DISPLAY INVERTIDO] Ventana Principal (APP) en monitor secundario (FÍSICO):', primaryDisplay.bounds);
        console.log('[DISPLAY INVERTIDO] Ventanas de Fondo (APP) en monitor principal (FÍSICO):', secondaryDisplay.bounds);
    } else {
        primaryDisplay = systemPrimary;
        secondaryDisplay = null;
        console.warn('[DISPLAY] Solo se detectó el monitor principal. Todas las ventanas irán aquí.');
    }
}

function getPrimaryDisplay() { return primaryDisplay; }
function getSecondaryDisplay() { return secondaryDisplay; }
// ------------------------------------------

function getIconFullPath() {
    const config = configManager.getConfig();
    if (config.resourcesDir && config.iconPath) {
        return path.join(config.resourcesDir, config.iconPath);
    }
    return undefined;
}

function saveWindowBounds(window) {
  if (!window || window.isDestroyed()) return;

const bounds = window.getBounds();

    try {
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

    fs.writeFileSync(configPath, JSON.stringify(config, null, 2), 'utf8');
    console.log('[CONFIG] Posicion guardada en config.json:', config.lastConfiguration.windowBounds);
  } catch (err) {
    console.error('[CONFIG ERROR] No se pudo guardar posicion:', err);
 }
}

function watchWindowPosition(window) {
  const save = () => saveWindowBounds(window);
  window.on('move', save);
  window.on('resize', save);
  window.on('close', save);
}

function createSelectorWindow() {
  if (appState.winSelector) return;

  const config = configManager.getConfig();
  const iconFullPath = getIconFullPath(); 

  const win = new BrowserWindow({
    width: 450,
     height: 650,
    frame: true,
    resizable: false,
    icon: iconFullPath,
    webPreferences: {
     preload: pathManager.preloadScript,
     contextIsolation: true,
     nodeIntegration: false,
     },
  });

  win.setMenu(null);
  win.loadFile(pathManager.selectorHtml);

  win.on('closed', () => {
    appState.winSelector = null;
    if (appState.windows.length === 0 && appState.backgroundWindows.length === 0) app.quit(); 
  });

  appState.winSelector = win;
}

function createWindow(bounds, isMain = false, htmlFile) { 
  const config = configManager.getConfig();
  const lastBounds = config?.lastConfiguration?.windowBounds;
  const iconFullPath = getIconFullPath(); 

  if (isMain && lastBounds && htmlFile === pathManager.indexHtml) {
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
    resizable: isMain, 
    alwaysOnTop: true,
    focusable: isMain,
    skipTaskbar: !isMain,
    backgroundColor: '#000000',
    hasShadow: false,
    icon: iconFullPath, 
    webPreferences: {
      preload: pathManager.preloadScript,
      contextIsolation: true,
      webSecurity: false,
    },
 });

  win.setAlwaysOnTop(true, 'screen-saver');

  win.loadFile(htmlFile);

  if (isMain) {
    win.setIgnoreMouseEvents(false);

    win.webContents.on('before-input-event', (event, input) => {
     if (input.control && input.shift && input.key.toLowerCase() === 'r') {
        console.log('[ATAJO] Ctrl+Shift+R detectado - Volviendo al selector');
        event.preventDefault();
        closeAllWindows(); 
        clearInactivityTimer();
        createSelectorWindow();
    }
    });

    watchWindowPosition(win);

  } else {
    // 🎯 AJUSTE FINAL: Forzar que el ratón NO sea ignorado.
    // Esto resuelve conflictos de composición en ciertos sistemas.
    win.setIgnoreMouseEvents(false); 
    win.focus(); // Forzar el render
    
    if (bounds.isFullScreen) {
         win.setFullScreen(true);
    }
 }

  if (bounds.index !== undefined) win.positionIndex = bounds.index;
  if (isMain) appState.windows.push(win);
  else appState.backgroundWindows.push(win);

  return win;
}

function closeAllWindows() {
    if (appState.winSelector && !appState.winSelector.isDestroyed()) { appState.winSelector.close(); }
    appState.winSelector = null; 

    appState.windows = appState.windows.filter(w => {
        if (w && !w.isDestroyed()) { w.close(); return false; } return false;
    });
    
    appState.backgroundWindows = appState.backgroundWindows.filter(w => {
        if (w && !w.isDestroyed()) { w.close(); return false; } return false;
    });
}

function getMainWindow() {
    const mainWin = appState.windows[0];
    if (mainWin && !mainWin.isDestroyed()) { return mainWin; }
    return null; 
}

module.exports = {
  createSelectorWindow,
  createWindow,
  closeAllWindows,
  getMainWindow,
  initializeDisplays,
  getPrimaryDisplay,
  getSecondaryDisplay
};