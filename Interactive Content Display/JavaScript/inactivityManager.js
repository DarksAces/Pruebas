// JavaScript/inactivityManager.js (CORREGIDO + LOGGING)

const fs = require('fs');
const appState = require('./appState');
const pathManager = require('./pathManager');
const { getConfig } = require('./configManager');
const logManager = require('./logManager'); 

// Ejecuta la acción de reseteo: borrar archivo y avisar al frontend
function resetToWelcome(mainWin) {
    if (fs.existsSync(pathManager.userFile)) {
        // Borramos 'contenido.txt' para simular estado vacío
        fs.unlink(pathManager.userFile, (err) => { 
            if (err) {
                console.error('Error al eliminar contenido.txt por inactividad:', err);
                logManager.logError('INACTIVITY_RESET_UNLINK', err); 
            } else {
                console.log('contenido.txt eliminado por inactividad. Volviendo a bienvenida.');
            }
            if (mainWin && !mainWin.isDestroyed()) {
                 mainWin.webContents.send('no-file', {});
            }
        });
    } else {
        if (mainWin && !mainWin.isDestroyed()) {
            mainWin.webContents.send('no-file', {});
        }
    }
}

// Inicia o reinicia el temporizador
function startInactivityTimer(mainWin) {
    const config = getConfig();
    if (!config) {
        console.error("[TEMPORIZADOR] Error: Configuración no cargada.");
        logManager.logError('INACTIVITY_START_CONFIG_FAIL', "Configuración no cargada."); 
        return;
    }
    const INACTIVITY_TIME_MS = config.inactivityTimeMs;

    clearInactivityTimer(); // Resetea el reloj anterior
    
    // Configura el nuevo timeout
    appState.inactivityTimer = setTimeout(() => {
        resetToWelcome(mainWin);
    }, INACTIVITY_TIME_MS);
    
    console.log(`[TEMPORIZADOR] Reiniciado. Reset en ${INACTIVITY_TIME_MS / 1000}s.`);
}

// Cancela el temporizador (ej: al cerrar la ventana)
function clearInactivityTimer() {
    if (appState.inactivityTimer) {
        clearTimeout(appState.inactivityTimer);
        appState.inactivityTimer = null;
    }
}

module.exports = {
    startInactivityTimer,
    clearInactivityTimer,
    resetToWelcome
};