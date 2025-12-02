// JavaScript/appState.js

module.exports = {
    winSelector: null,  // Referencia a la ventana de configuración inicial (Selector).
    windows: [],        // Array que almacena todas las ventanas activas (Video Principal y Fondos).
    inactivityTimer: null // Referencia al setTimeout del temporizador de inactividad para poder cancelarlo/reiniciarlo.
};