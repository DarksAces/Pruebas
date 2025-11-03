// JavaScript/appState.js

/*
 * Estado global de la aplicación (memoria compartida entre módulos del proceso main).
 * Este módulo exporta un objeto simple que contiene referencias a ventanas y timers.
 * No contiene lógica, sólo valores mutables que otros módulos leen/escriben.
 *
 * Campos:
 *  - winSelector: BrowserWindow | null -> referencia a la ventana del selector (UI)
 *  - windows: Array<BrowserWindow> -> lista de ventanas creadas (main + fondos)
 *  - inactivityTimer: Timeout | null -> referencia al temporizador para inactividad
 *
 * Nota: Se mantiene deliberadamente minimalista para evitar sincronización compleja.
 */

module.exports = {
    // Referencia a la ventana del selector (si está abierta)
    winSelector: null,

    // Lista de ventanas activas (main + ventanas de fondo)
    windows: [],

    // Temporizador de inactividad (si se usa)
    inactivityTimer: null
};