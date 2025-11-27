// JavaScript/inactivityManager.js (CORREGIDO + LOGGING)

const fs = require('fs');
const appState = require('./appState');
const pathManager = require('./pathManager');
const { getConfig } = require('./configManager');
const logManager = require('./logManager'); // <-- ¡IMPORTADO!

// NO definimos INACTIVITY_TIME_MS aquí arriba

function resetToWelcome(mainWin) {
    if (fs.existsSync(pathManager.userFile)) {
        fs.unlink(pathManager.userFile, (err) => { 
            if (err) {
                console.error('Error al eliminar contenido.txt por inactividad:', err);
                logManager.logError('INACTIVITY_RESET_UNLINK', err); // <-- ¡LOGGING AÑADIDO!
            } else {
                console.log('contenido.txt eliminado por inactividad. Volviendo a bienvenida.');
            }
            if (mainWin && !mainWin.isDestroyed()) {
                 // ******************************************************
                 // CORRECCIÓN: Se envía un objeto vacío, eliminando welcomePath
                 mainWin.webContents.send('no-file', {});
                 // ******************************************************
            }
        });
    } else {
        if (mainWin && !mainWin.isDestroyed()) {
            // ******************************************************
            // CORRECCIÓN: Se envía un objeto vacío, eliminando welcomePath
            mainWin.webContents.send('no-file', {});
            // ******************************************************
        }
    }
}

function startInactivityTimer(mainWin) {
    // Obtenemos la configuración AQUÍ, cuando la función es llamada
    const config = getConfig();
    if (!config) {
        console.error("[TEMPORIZADOR] Error: Configuración no cargada. No se puede iniciar el temporizador.");
        logManager.logError('INACTIVITY_START_CONFIG_FAIL', "Configuración no cargada."); // <-- ¡LOGGING AÑADIDO!
        return;
    }
    const INACTIVITY_TIME_MS = config.inactivityTimeMs;

    clearInactivityTimer(); // Limpiar cualquier temporizador anterior
    
    appState.inactivityTimer = setTimeout(() => {
        resetToWelcome(mainWin);
    }, INACTIVITY_TIME_MS);
    
    console.log(`[TEMPORIZADOR] Reiniciado. El archivo se eliminara en ${INACTIVITY_TIME_MS / 1000} segundos si no hay cambios.`);
}

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