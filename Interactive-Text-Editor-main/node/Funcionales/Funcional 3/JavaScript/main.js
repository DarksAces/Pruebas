// JavaScript/main.js
// ============================================================================
// TODO EN LA CARPETA DE INSTALACIÓN -> SUBDIRECTORIO RESOURCES
// ============================================================================

const { app, ipcMain } = require('electron');
const path = require('path');
const fs = require('fs'); 
const configManager = require('./configManager');
const windowManager = require('./windowManager');
const { registerHandlers } = require('./ipcHandlers');
const logManager = require('./logManager'); 

// ============================================================================
// DIRECTORIO DE DATOS = DONDE SE INSTALE LA APP
// ============================================================================
const DATA_DIR = path.dirname(process.execPath); // Carpeta raíz del .exe
const CONFIG_FILENAME = 'InteractiveContentDisplay.json';

console.log('========================================');
console.log(`DATA DIR: ${DATA_DIR}`);
console.log('========================================');

// Crear carpeta DATA_DIR si no existe (por seguridad)
if (!fs.existsSync(DATA_DIR)) {
    fs.mkdirSync(DATA_DIR, { recursive: true });
    console.log(`✓ Carpeta DATA_DIR creada`);
}

// Globalizar para que otros módulos lo usen
global.DATA_DIR = DATA_DIR;

// ============================================================================
// CARGAR CONFIGURACIÓN
// ============================================================================
try {
    // ------------------------------------------------------------------------
    // CORRECCIÓN: Definir carpeta 'resources' dentro del directorio de instalación
    // ------------------------------------------------------------------------
    const resourcesDir = path.join(DATA_DIR, 'resources');

    // Crear la carpeta 'resources' si no existe
    if (!fs.existsSync(resourcesDir)) {
        fs.mkdirSync(resourcesDir, { recursive: true });
        console.log(`✓ Carpeta 'resources' creada en: ${resourcesDir}`);
    }

    // Definir la ruta del config DENTRO de 'resources'
    const userConfigPath = path.join(resourcesDir, CONFIG_FILENAME);
    
    // Si no existe el archivo config en resources, copiarlo desde el source original
    if (!fs.existsSync(userConfigPath)) {
        let sourceConfigPath;
        
        if (app.isPackaged) {
            // Producción: buscar en resources.asar/config
            sourceConfigPath = path.join(path.dirname(process.execPath), 'resources', 'app.asar', 'config', CONFIG_FILENAME);
            
            // Fallback: Si no está en asar, buscar en la raíz junto al exe
            if (!fs.existsSync(sourceConfigPath)) {
                sourceConfigPath = path.join(path.dirname(process.execPath), CONFIG_FILENAME);
            }
        } else {
            // Desarrollo: buscar en la carpeta del proyecto ../config/
            sourceConfigPath = path.join(__dirname, '..', 'config', CONFIG_FILENAME);
        }
        
        if (fs.existsSync(sourceConfigPath)) {
            fs.copyFileSync(sourceConfigPath, userConfigPath);
            console.log(`✓ Config copiado exitosamente a: ${userConfigPath}`);
        } else {
            throw new Error(`Config base no encontrado en: ${sourceConfigPath}`);
        }
    } else {
        console.log(`✓ El archivo Config ya existe en: ${userConfigPath}`);
    }
    
    // Cargar configuración desde la nueva ruta en 'resources'
    configManager.loadConfig(userConfigPath);
    console.log(`✓ Config cargado en memoria desde: ${userConfigPath}`);
    
    // ========================================================================
    // INICIALIZAR LOGS
    // ========================================================================
    const config = configManager.getConfig();
    // Los logs se guardarán donde diga el config (relativo a DATA_DIR)
    const logsDir = path.join(DATA_DIR, config.logFilePath);
    
    logManager.initializeLog(logsDir);
    console.log(`✓ Logs inicializados en: ${logsDir}`);
    
    logManager.log('INFO', 'STARTUP', `APP STARTED - Config path: ${userConfigPath}`);

} catch (error) {
    console.error('[FATAL STARTUP ERROR]', error.message);
    if (logManager && logManager.logError) {
        // Intentar loguear si logManager alcanzó a cargar, sino solo consola
        try { logManager.logError('MAIN_FATAL', error); } catch(e){}
    }
    app.quit();
    process.exit(1);
}

// ============================================================================
// REGISTRAR HANDLERS (Eventos IPC)
// ============================================================================
registerHandlers();

// ============================================================================
// INICIAR APP
// ============================================================================
app.whenReady().then(() => {
    // Intentar cargar la última sesión guardada en el config
    const lastConfig = configManager.loadLastConfig();
    
    if (lastConfig && lastConfig.size) {
        console.log('✓ Restaurando sesión previa automáticamente...');
        
        // Usamos nextTick para dar un respiro al event loop y asegurar que ipcMain esté listo
        process.nextTick(() => {
            // Emitimos manualmente el evento 'selection-made' hacia nosotros mismos (ipcMain)
            // null es el 'event' (no necesario aquí), lastConfig son los datos
            ipcMain.emit('selection-made', null, lastConfig);
        });
    } else {
        console.log('✓ Sin sesión previa o config vacío. Abriendo Selector.');
        windowManager.createSelectorWindow();
    }
});

app.on('window-all-closed', () => {
    // En Windows cerramos la app cuando no quedan ventanas. 
    // En macOS es común dejarla activa en el dock (darwin).
    if (process.platform !== 'darwin') app.quit();
});