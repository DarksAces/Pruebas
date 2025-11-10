// JavaScript/appState.js

module.exports = {
    winSelector: null,  // La ventana del selector
    windows: [],        // Array de ventanas de contenido principal (solo index.html)
    // 🎯 CORRECCIÓN: Agregar el array para las ventanas de fondo
    backgroundWindows: [], 
    inactivityTimer: null // Referencia al temporizador de inactividad
};