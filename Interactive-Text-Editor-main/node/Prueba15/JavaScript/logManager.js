// JavaScript/logManager.js (VERSIÓN FINAL DEFINITIVA)

const fs = require('fs');
const path = require('path');
const pathManager = require('./pathManager');

let _logPath = null; // <-- CACHE PARA LA RUTA

// Definiciones de constantes (7 días)
const MAX_AGE_MS = 7 * 24 * 60 * 60 * 1000; 
const ROTATED_LOG_PATTERN = /^app_\d{8}_\d{4}\.log$/; 

// --- cleanOldLogs y rotateLogFile usan _logPath (omitiendo su cuerpo para brevedad) ---

function cleanOldLogs() {
    // ... (El cuerpo usa _logPath)
    try {
        const logDir = path.dirname(_logPath); 
        // ... (Lógica de limpieza)
    } catch (error) {
        console.error(`[LOG CLEANUP FATAL ERROR] Falló la limpieza de logs. Error: ${error.message}`);
    }
}

function rotateLogFile() {
    // ... (El cuerpo usa _logPath)
    try {
        // ... (Lógica de renombrado usando _logPath)
    } catch (error) {
        console.error(`[LOG ROTATION FAILED] No se pudo rotar el log. Detalle del Error: ${error.message}`);
    }
}

// --- FUNCIÓN DE LOG PRINCIPAL (log) ---
function log(level, context, message) {
    const timestamp = new Date().toISOString();
    
    let logMessage;
    if (level === 'ERROR' || level === 'FATAL') {
        logMessage = (message instanceof Error) ? (message.stack || message.message) : String(message);
    } else {
        logMessage = String(message);
    }

    // *** DECLARACIÓN FUERA DEL TRY PARA EVITAR EL ERROR "logEntry is not defined" ***
    const logEntry = `[${timestamp}] [${level}] [${context}] ${logMessage}\n`;
    
    // 1. Mostrar en consola
    if (level === 'ERROR' || level === 'FATAL') {
        console.error(logEntry.trim());
    } else {
        console.log(logEntry.trim());
    }
    
    try {
        // 2. **VERIFICACIÓN CRÍTICA**
        if (!_logPath) {
             console.error(`[LOG MANAGER FATAL] Fallo en la escritura: logPath no está definido. Contexto: ${context}`);
             return; 
        }

        // 3. Asegurarse de que el directorio exista
        const logDir = path.dirname(_logPath);
        if (!fs.existsSync(logDir)) {
            fs.mkdirSync(logDir, { recursive: true });
        }

        // 4. Escribir al archivo
        fs.appendFileSync(_logPath, logEntry, 'utf-8');
        
    } catch (logErr) {
        // Si la escritura falla por permisos, reportamos el error de I/O
        console.error(`[LOG MANAGER FATAL] No se pudo escribir en el log. Error interno: ${logErr.message}. Mensaje que se perdió: ${logEntry.trim()}`);
    }
}

// --- FUNCIÓN DE INICIALIZACIÓN PÚBLICA (Recibe la ruta) ---
function initializeLog(filePath) {
    if (!filePath || typeof filePath !== 'string') {
        console.error("[LOG MANAGER FATAL] Initialize Log requiere una ruta de archivo válida.");
        return;
    }
    _logPath = filePath; // <-- ¡ESTABLECE LA RUTA CACHEADA!
    
    rotateLogFile();
    cleanOldLogs();
}

// ----------------------------------------------------
module.exports = {
    log,
    logError: (context, error) => log('ERROR', context, error),
    logFatal: (context, error) => log('FATAL', context, error),
    initializeLog 
};