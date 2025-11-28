// JavaScript/logManager.js (MODIFICADO para log diario)

const fs = require('fs');
const path = require('path');
const pathManager = require('./pathManager'); // Se mantiene

let _logFilePath = null; // <-- Ahora almacena la RUTA COMPLETA del archivo de log del día

// Definiciones de constantes (7 días)
const MAX_AGE_MS = 7 * 24 * 60 * 60 * 1000; 
// Expresión regular para logs rotados o diarios antiguos (ej: 2025-11-28.log)
const LOG_FILE_PATTERN = /^\d{4}-\d{2}-\d{2}\.log$/; 

/**
 * Genera la ruta completa del archivo de log para el día actual.
 * El formato del nombre será AAAA-MM-DD.log (ej: 2025-11-28.log)
 * @param {string} logDir La ruta base del directorio de logs (C:\recursos\log)
 * @returns {string} La ruta completa del archivo de log diario.
 */
function getDailyLogFilePath(logDir) {
    const now = new Date();
    const datePart = now.toISOString().split('T')[0]; // Formato YYYY-MM-DD
    const fileName = `${datePart}.log`;
    return path.join(logDir, fileName);
}


/**
 * Limpia archivos de log más antiguos que MAX_AGE_MS (7 días).
 */
function cleanOldLogs(logDir) {
    if (!fs.existsSync(logDir)) return;
    
    const cutoff = Date.now() - MAX_AGE_MS;
    
    try {
        const files = fs.readdirSync(logDir);
        
        files.forEach(file => {
            if (LOG_FILE_PATTERN.test(file)) {
                const filePath = path.join(logDir, file);
                const stats = fs.statSync(filePath);
                
                // Usamos mtime (tiempo de modificación) para determinar la edad
                if (stats.mtimeMs < cutoff) {
                    fs.unlinkSync(filePath);
                    console.log(`[LOG CLEANUP] Eliminado log antiguo: ${file}`);
                }
            }
        });
    } catch (error) {
        console.error(`[LOG CLEANUP FATAL ERROR] Falló la limpieza de logs en ${logDir}. Error: ${error.message}`);
    }
}

// NOTE: rotateLogFile() se elimina porque la funcionalidad de log diario la reemplaza.

// --- FUNCIÓN DE LOG PRINCIPAL (log) ---
function log(level, context, message) {
    const timestamp = new Date().toISOString();
    
    let logMessage;
    if (level === 'ERROR' || level === 'FATAL') {
        // Para errores, aseguramos que el mensaje sea la pila o el mensaje de error
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
        // Ahora usamos _logFilePath que YA contiene el nombre del archivo diario
        if (!_logFilePath) {
             console.error(`[LOG MANAGER FATAL] Fallo en la escritura: logFilePath no está definido. Contexto: ${context}`);
             return; 
        }

        // 3. Asegurarse de que el directorio exista
        const logDir = path.dirname(_logFilePath);
        if (!fs.existsSync(logDir)) {
            fs.mkdirSync(logDir, { recursive: true });
        }

        // 4. Escribir al archivo
        fs.appendFileSync(_logFilePath, logEntry, 'utf-8');
        
    } catch (logErr) {
        // Si la escritura falla por permisos, reportamos el error de I/O
        console.error(`[LOG MANAGER FATAL] No se pudo escribir en el log. Error interno: ${logErr.message}. Mensaje que se perdió: ${logEntry.trim()}`);
    }
}

// --- FUNCIÓN DE INICIALIZACIÓN PÚBLICA (Recibe la ruta del Directorio) ---
function initializeLog(logDir) {
    if (!logDir || typeof logDir !== 'string') {
        console.error("[LOG MANAGER FATAL] Initialize Log requiere una ruta de directorio válida.");
        return;
    }
    
    // 1. Genera la ruta completa del archivo de log diario y la almacena.
    _logFilePath = getDailyLogFilePath(logDir); 
    
    // 2. Limpia los logs antiguos
    cleanOldLogs(logDir);
}

// ----------------------------------------------------
module.exports = {
    log,
    logError: (context, error) => log('ERROR', context, error),
    logFatal: (context, error) => log('FATAL', context, error),
    initializeLog 
};