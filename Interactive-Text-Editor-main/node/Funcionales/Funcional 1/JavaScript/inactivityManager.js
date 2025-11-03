// JavaScript/inactivityManager.js

/*
 * Módulo para gestionar comportamiento por inactividad.
 * Uso típico:
 *  - startInactivityTimer(mainWin) -> inicia o reinicia el temporizador con la duración de config
 *  - clearInactivityTimer() -> limpia el temporizador si existe
 *  - resetToWelcome(mainWin) -> fuerza la eliminación del archivo de usuario y envía 'no-file'
 *
 * Requisitos:
 *  - `configManager.loadConfig()` debe haberse ejecutado antes de llamar startInactivityTimer
 *  - `pathManager` expone rutas como userFile y welcomeImage
 */

const fs = require('fs');
const appState = require('./appState');
const pathManager = require('./pathManager');
const { getConfig } = require('./configManager');

// Nota: No definimos INACTIVITY_TIME_MS como constante en el módulo porque su valor
// puede venir de la configuración que se carga en tiempo de ejecución.

function resetToWelcome(mainWin) {
    // Si existe el archivo de usuario, eliminarlo. Esto sirve para "resetear" la pantalla
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
        // Si no existe el archivo, simplemente notificamos al renderer para que muestre bienvenida
        if (mainWin && !mainWin.isDestroyed()) {
            mainWin.webContents.send('no-file', {
                welcomePath: pathManager.getFileUrl(pathManager.welcomeImage)
            });
        }
    }
}

function startInactivityTimer(mainWin) {
    // Obtenemos la configuración cuando la función es llamada (puede cambiar entre ejecuciones)
    const config = getConfig();
    if (!config) {
        console.error("[TEMPORIZADOR] Error: Configuración no cargada. No se puede iniciar el temporizador.");
        return;
    }
    const INACTIVITY_TIME_MS = config.inactivityTimeMs;

    // Limpiar posibles temporizadores previos antes de arrancar uno nuevo
    clearInactivityTimer(); 
    
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