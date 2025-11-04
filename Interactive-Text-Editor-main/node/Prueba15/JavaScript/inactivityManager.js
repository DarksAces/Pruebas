// JavaScript/inactivityManager.js

const fs = require('fs');
const appState = require('./appState');
const pathManager = require('./pathManager');
const { getConfig } = require('./configManager');

// NO definimos INACTIVITY_TIME_MS aquí arriba

function resetToWelcome(mainWin) {
    if (fs.existsSync(pathManager.userFile)) {
        fs.unlink(pathManager.userFile, (err) => { 
            if (err) {
                console.error('Error al eliminar contenido.txt por inactividad:', err);
            } else {
                console.log('contenido.txt eliminado por inactividad. Volviendo a bienvenida.');
            }
            if (mainWin && !mainWin.isDestroyed()) {
                 mainWin.webContents.send('no-file', {
                     welcomePath: pathManager.getFileUrl(pathManager.welcomeImage)
                 });
            }
        });
    } else {
        if (mainWin && !mainWin.isDestroyed()) {
            mainWin.webContents.send('no-file', {
                welcomePath: pathManager.getFileUrl(pathManager.welcomeImage)
            });
        }
    }
}

function startInactivityTimer(mainWin) {
    // Obtenemos la configuración AQUÍ, cuando la función es llamada
    const config = getConfig();
    if (!config) {
        console.error("[TEMPORIZADOR] Error: Configuración no cargada. No se puede iniciar el temporizador.");
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