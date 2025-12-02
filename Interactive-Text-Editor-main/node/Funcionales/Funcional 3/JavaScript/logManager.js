// JavaScript/logManager.js (MODIFICADO para log diario)

const fs = require('fs');
const path = require('path');
const pathManager = require('./pathManager'); // Se mantiene

let _logFilePath = null; // <-- Almacena la RUTA COMPLETA del archivo de log específico para HOY.

// Definiciones de constantes (7 días en milisegundos)
const MAX_AGE_MS = 7 * 24 * 60 * 60 * 1000; 
// Expresión regular para identificar archivos de log válidos (formato AAAA-MM-DD.log)
const LOG_FILE_PATTERN = /^\d{4}-\d{2}-\d{2}\.log$/; 

/**
 * Genera la ruta del archivo basado en la fecha actual.
 * @param {string} logDir La ruta base del directorio de logs.
 * @returns {string} Ruta completa ej: C:\recursos\log\2025-11-28.log
 */
function getDailyLogFilePath(logDir) {
    const now = new Date();
    const datePart = now.toISOString().split('T')[0]; // Extrae solo YYYY-MM-DD
    const fileName = `${datePart}.log`;
    return path.join(logDir, fileName);
}


/**
 * Limpieza automática: Elimina logs que tengan más de 7 días de antigüedad.
 * Se ejecuta al iniciar la aplicación.
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
                
                // Compara la fecha de modificación del archivo con la fecha de corte
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

// --- FUNCIÓN DE LOG PRINCIPAL ---
// Escribe el mensaje tanto en la consola (para debug en vivo) como en el archivo físico.
function log(level, context, message) {
    const timestamp = new Date().toISOString();
    
    let logMessage;
    // Si es un error real, extraemos el stack trace para mejor diagnóstico
    if (level === 'ERROR' || level === 'FATAL') {
        logMessage = (message instanceof Error) ? (message.stack || message.message) : String(message);
    } else {
        logMessage = String(message);
    }

    // Formato del log: [FECHA] [NIVEL] [CONTEXTO] Mensaje
    const logEntry = `[${timestamp}] [${level}] [${context}] ${logMessage}\n`;
    
    // 1. Mostrar en consola del sistema
    if (level === 'ERROR' || level === 'FATAL') {
        console.error(logEntry.trim());
    } else {
        console.log(logEntry.trim());
    }
    
    try {
        // 2. **VERIFICACIÓN DE SEGURIDAD**
        if (!_logFilePath) {
             console.error(`[LOG MANAGER FATAL] Fallo en la escritura: logFilePath no está definido. Contexto: ${context}`);
             return; 
        }

        // 3. Crear directorio si no existe
        const logDir = path.dirname(_logFilePath);
        if (!fs.existsSync(logDir)) {
            fs.mkdirSync(logDir, { recursive: true });
        }

        // 4. Escribir al archivo (append para no borrar lo anterior)
        fs.appendFileSync(_logFilePath, logEntry, 'utf-8');
        
    } catch (logErr) {
        // Capturamos errores de I/O (disco lleno, permisos) para que la app no crashee por culpa del log
        console.error(`[LOG MANAGER FATAL] No se pudo escribir en el log. Error interno: ${logErr.message}. Mensaje que se perdió: ${logEntry.trim()}`);
    }
}

// --- INICIALIZACIÓN ---
// Debe llamarse desde main.js una vez cargada la configuración.
function initializeLog(logDir) {
    if (!logDir || typeof logDir !== 'string') {
        console.error("[LOG MANAGER FATAL] Initialize Log requiere una ruta de directorio válida.");
        return;
    }
    
    // 1. Establece dónde se escribirá hoy
    _logFilePath = getDailyLogFilePath(logDir); 
    
    // 2. Ejecuta la limpieza de archivos viejos
    cleanOldLogs(logDir);
}

// Exportación de métodos
module.exports = {
    log,
    logError: (context, error) => log('ERROR', context, error),
    logFatal: (context, error) => log('FATAL', context, error),
    initializeLog 
};