# Interactive Text Editor - Funcional 2 (Versión Modular & Escalable)

Aplicación Electron completamente modular para gestión de contenido interactivo con múltiples ventanas, posicionamiento dinámico, e inactividad automática. Construida con una arquitectura de componentes independientes que facilita mantenimiento, testing y escalabilidad.

---

## 🚀 Inicio Rápido

### ⚙️ 1. Instalar Node.js y npm

#### **Windows**

1. **Descargar Node.js**:
   - Ir a: https://nodejs.org/
   - Descargar versión **LTS** (Long Term Support)
   - Ejecutar instalador `.msi`

2. **Instalar Node.js**:
   - Seguir pasos del instalador
   - Seleccionar "Add to PATH" (importante)
   - Reiniciar la computadora

3. **Verificar instalación**:
   ```powershell
   node --version     # Debe mostrar v14.0.0 o superior
   npm --version      # Debe mostrar v6.0.0 o superior
   ```

#### **macOS**

```bash
# Usar Homebrew (recomendado)
brew install node

# Verificar
node --version
npm --version
```

#### **Linux (Ubuntu/Debian)**

```bash
# Actualizar paquetes
sudo apt update

# Instalar Node.js y npm
sudo apt install nodejs npm

# Verificar
node --version
npm --version
```

---

### 📦 2. Instalar Dependencias del Proyecto

```powershell
# Navegar a la carpeta del proyecto
cd "C:\Users\Daniel\Documents\GitHub\Scripts-Prueba\Interactive-Text-Editor-main\node\Prueba15"

# Instalar dependencias (electron, electron-builder, etc.)
npm install

# Verificar que se instalaron correctamente
npm list
# Debe mostrar:
# ├── electron@28.2.1
# └── electron-builder@24.9.1
```

**¿Qué se instala?**
- `electron` - Framework para apps de escritorio
- `electron-builder` - Herramienta para compilar ejecutables
- Otras dependencias necesarias

**Tiempo estimado**: 2-5 minutos (depende de conexión)

---

### ▶️ 3. Comandos Principales

#### **Ejecutar en Desarrollo**

```powershell
npm start
```

**Qué pasa:**
- ✅ Abre la aplicación en modo desarrollo
- ✅ DevTools disponibles (Ctrl+Shift+I)
- ✅ Ver logs en consola
- ✅ Cambios en código se reflejan al recargar (F5)

#### **Compilar Ejecutable (Windows)**

```powershell
npm run dist
```

**O también:**

```powershell
npm run build:win
```

**Qué pasa:**
- ✅ Compila la aplicación
- ✅ Genera instalador `.nsis` en carpeta `dist/`
- ✅ Genera archivo `.exe` ejecutable directo
- ✅ Archivo listo para distribuir a usuarios

**Ubicación del .exe:**
```
Prueba15/dist/
├── Interactive Content Editor Setup 1.0.0.exe   # Instalador
└── Interactive Content Editor 1.0.0.exe         # Ejecutable directo
```

**Tiempo estimado**: 3-5 minutos

#### **Compilar para macOS**

```powershell
npm run build:mac
```

Genera archivo `.dmg` para instalar en Mac.

#### **Compilar para Linux**

```powershell
npm run dist
```

Genera `.AppImage`, `.deb`, etc.

---

### 🔧 4. Solución Rápida si Hay Problemas

```powershell
# 1. Borrar dependencias
Remove-Item -Recurse node_modules

# 2. Borrar cache de npm
npm cache clean --force

# 3. Reinstalar todo
npm install

# 4. Intentar ejecutar nuevamente
npm start
```

---

## 📋 Tabla de Contenidos

1. [Descripción General](#descripción-general)
2. [Estructura del Proyecto](#estructura-del-proyecto)
3. [Detalles de cada Módulo](#detalles-de-cada-módulo)
4. [Configuración](#configuración)
5. [Flujo de Ejecución](#flujo-de-ejecución)
6. [Instalación y Uso](#instalación-y-uso)
7. [Interfaz de Usuario](#interfaz-de-usuario)
8. [Sistema de Logs](#sistema-de-logs)
9. [Características Avanzadas](#características-avanzadas)
10. [Solución de Problemas](#solución-de-problemas)
11. [Desarrollo y Extensión](#desarrollo-y-extensión)

---

## 🎯 Descripción General

**Interactive Text Editor** es una aplicación de escritorio construida con **Electron** que permite:

- **Gestión de múltiples ventanas** con posicionamiento dinámico (pantalla completa, mitades, cuartos)
- **Soporte multi-monitor** con cálculos precisos de posiciones
- **Auto-reset por inactividad** con temporizador configurable
- **Persistencia de sesión** - guarda última configuración usada
- **Sistema de logging avanzado** con rotación de archivos
- **Arquitectura modular** - 9 módulos especializados sin acoplamiento
- **Comunicación IPC segura** entre procesos principal y renderizado
- **Preload script** para aislamiento de contexto en ventanas

### ¿Por qué modular?

La separación en módulos permite:
- **Mantenibilidad**: Cambios en un módulo no afectan otros
- **Testabilidad**: Cada módulo puede probarse independientemente
- **Escalabilidad**: Agregar nuevas características sin reescribir código existente
- **Reutilización**: Los módulos pueden importarse en otros proyectos

---

## 📁 Estructura del Proyecto

```
Prueba15/
│
├── package.json                    # Dependencias y scripts de Node.js
├── package-lock.json               # Versiones exactas de dependencias
├── ReadMe.md                        # Este archivo
├── .gitignore                       # Archivos ignorados por Git
│
├── config/
│   └── config.json                 # Configuración centralizada (EXPLICADO ABAJO)
│
├── html/                           # Interfaz de Usuario - Archivos HTML
│   ├── selector.html               # Ventana selector (configuración inicial)
│   ├── index.html                  # Ventana principal de contenido
│   └── background.html             # Ventana de fondo (soporte)
│
├── JavaScript/                     # Lógica de la aplicación (Módulos)
│   ├── main.js                     # Punto de entrada de Electron (orquestación)
│   ├── appState.js                 # Estado global compartido entre módulos
│   ├── configManager.js            # Carga/guarda/gestiona configuración
│   ├── pathManager.js              # Resuelve rutas de recursos multiplataforma
│   ├── windowManager.js            # Crea y gestiona ventanas
│   ├── positionCalculator.js       # Calcula posiciones precisas de ventanas
│   ├── inactivityManager.js        # Temporizador de inactividad y reset
│   ├── ipcHandlers.js              # Registra todos los manejadores IPC
│   ├── preload.js                  # Script de seguridad para renderers
│   └── logManager.js               # Sistema de logging con rotación
│
├── dist/                           # Ejecutable compilado (generado por electron-builder)
│   └── [exe, msi, nsis, etc.]     # Binarios empaquetados
│
└── node_modules/                   # Dependencias instaladas (electron, electron-builder, etc.)
```

---

## 🔧 Detalles de cada Módulo

### 1. **main.js** - Punto de Entrada (Orquestador)

**Responsabilidad**: Inicializar la aplicación, cargar configuración, registrar IPC, y orquestar el ciclo de vida.

**¿Qué hace exactamente?**

```
1. FASE DE INICIALIZACIÓN:
   ├─ Resuelve rutas de configuración
   ├─ Si es .EXE (empaquetado):
   │  └─ Copia config.json a AppData (para poder modificarlo)
   ├─ Carga configManager
   └─ Inicializa el sistema de logs

2. FASE DE REGISTRO IPC:
   └─ Llama a registerHandlers() de ipcHandlers.js

3. FASE DE ARRANQUE:
   ├─ app.whenReady() dispara:
   │  ├─ Intenta cargar última configuración
   │  ├─ Si existe: restaura automáticamente (sin selector)
   │  └─ Si no existe: abre ventana selector
   │
   └─ Emite evento internal 'selection-made'

4. FASE DE CIERRE:
   └─ app.on('window-all-closed'):
      ├─ En Windows/Linux: quit()
      ├─ En macOS: espera Cmd+Q del usuario
      └─ Guarda logs finales
```

**Archivos relacionados**:
- `configManager.js` - para cargar/guardar config
- `windowManager.js` - para crear ventanas
- `ipcHandlers.js` - para registrar listeners
- `logManager.js` - para logging

**Error crítico**: Si config.json no se puede cargar → app.quit() inmediatamente

---

### 2. **appState.js** - Estado Global

**Responsabilidad**: Almacenar referencias a todas las ventanas y timers de la aplicación.

```javascript
module.exports = {
    winSelector: null,           // Referencia a ventana selector (solo 1)
    windows: [],                 // Array de ventanas activas [mainWindow, bgWindow1, bgWindow2...]
    inactivityTimer: null        // Referencia a setTimeout para poder cancelarlo cuando hay actividad
};
```

**¿Por qué centralizar estado?**
- **Acceso global**: Todos los módulos pueden consultar/modificar sin pasar parámetros
- **Sincronización**: Cambios en windowManager se reflejan en inactivityManager
- **Debug**: Ver appState en DevTools muestra estado actual

**Uso en otros módulos**:
```javascript
const appState = require('./appState');

// En windowManager.js:
appState.windows.push(newWindow);

// En inactivityManager.js:
appState.inactivityTimer = setTimeout(...);

// En cualquier lugar:
if (appState.windows.length > 0) { ... }
```

---

### 3. **configManager.js** - Gestión de Configuración

**Responsabilidad**: Cargar, guardar y gestionar la configuración persistente.

**¿Qué guarda?**

Dos tipos de datos:
1. **Configuración base** (config.json):
   - Rutas de directorios
   - Tiempos de inactividad
   - Configuraciones de sistema

2. **Última sesión** (lastConfig guardado):
   - Tamaño de ventana elegido (completa, 1/2, 1/4)
   - Posición (arriba, abajo, izquierda, derecha)
   - Para restauración automática

**Funciones principales**:

```javascript
configManager.loadConfig(filePath)
// Carga config.json desde archivo. Se ejecuta en main.js

configManager.getConfig()
// Retorna objeto de configuración actual
// Ejemplo: config.inactivityTimeMs = 3000

configManager.loadLastConfig()
// Retorna { size: '1/2', position: 'left' } si existe sesión anterior
// O null si es primer inicio

configManager.saveLastConfig(config)
// Guarda nueva sesión. Se ejecuta cuando usuario elige tamaño en selector
```

**Ubicación de archivos**:
- **Modo desarrollo**: `./config/config.json` (relativo)
- **Modo producción (.EXE)**: `C:\Users\Usuario\AppData\Roaming\AppName\config.json` (editable)

**¿Por qué AppData?**
- El .EXE está en `C:\Program Files\...` que es de solo lectura
- Necesitamos guardar cambios (última sesión)
- AppData es la ubicación estándar para datos de usuario en Windows

---

### 4. **pathManager.js** - Gestión de Rutas

**Responsabilidad**: Resolver rutas de archivos multiplataforma (Windows, macOS, Linux).

**¿Por qué es necesario?**

Problema: Las rutas difieren entre sistemas operativos:
- Windows: `C:\User\app\resources\image.png` (backslashes)
- Unix: `/home/user/app/resources/image.png` (forward slashes)
- Rutas relativas vs absolutas

**Solución**: pathManager usa `path.join()` que detecta el SO automáticamente.

**Rutas resueltas**:

```javascript
pathManager.preloadScript
// Devuelve ruta a preload.js (seguridad)
// Windows: C:\app\JavaScript\preload.js
// Unix: /app/JavaScript/preload.js

pathManager.selectorHtml
// Ruta a selector.html (ventana inicial)

pathManager.mainHtml
// Ruta a index.html (ventana principal)

pathManager.backgroundHtml
// Ruta a background.html (soporte)
```

**Implementación típica**:

```javascript
const path = require('path');

module.exports = {
    preloadScript: path.join(__dirname, 'preload.js'),
    selectorHtml: path.join(__dirname, '..', 'html', 'selector.html'),
    mainHtml: path.join(__dirname, '..', 'html', 'index.html'),
    // ... más rutas
};
```

**Beneficio**: El código funciona igual en todas las plataformas sin ajustes manuales.

---

### 5. **windowManager.js** - Gestión de Ventanas

**Responsabilidad**: Crear, configurar y gestionar todas las ventanas de la aplicación.

**Tipos de ventanas**:

1. **Ventana Selector** (createSelectorWindow):
   - Tamaño fijo: 450x650px
   - Con marco (frame: true)
   - No redimensionable
   - Usuario elige tamaño/posición aquí
   - Si se cierra sin elegir → app.quit()

2. **Ventana Principal** (createMainWindow):
   - Tamaño calculado por positionCalculator
   - Sin marco (frameless: true) para apariencia limpia
   - Contenido visible al usuario
   - Muestra archivos/contenido

3. **Ventanas de Fondo** (createBackgroundWindow):
   - Renderiza fondos sincronizados
   - Detrás de la ventana principal
   - Pueden ser múltiples (una por monitor)

**Flujo de creación**:

```
app inicia
    ↓
¿Hay última sesión guardada?
    ├─ SÍ: mainWindow creada automáticamente
    └─ NO: createSelectorWindow()
        ↓
    Usuario elige tamaño
        ↓
    IPC 'selection-made'
        ↓
    createMainWindow() con posición calculada
        ↓
    createBackgroundWindow() si es necesario
```

**Configuración de seguridad** (webPreferences):

```javascript
webPreferences: {
    preload: pathManager.preloadScript,  // Inyecta API segura
    contextIsolation: true,              // Proceso aislado
    nodeIntegration: false,              // No acceso a require()
    enableRemoteModule: false,           // Sin acceso a remote
    sandbox: true                        // Sandboxing activo
}
```

**Eventos**:

```javascript
// Cuando ventana se cierra
win.on('closed', () => {
    appState.windows = appState.windows.filter(w => w !== win);
    if (appState.windows.length === 0) {
        // Si no hay más ventanas, mostrar selector nuevamente
        windowManager.createSelectorWindow();
    }
});
```

---

### 6. **positionCalculator.js** - Cálculo de Posiciones

**Responsabilidad**: Calcular posiciones precisas de ventanas según tamaño, monitor, y bordes.

**¿Qué calcula?**

Dado:
- `size`: '1/1' (completa), '1/2' (mitad), '1/4' (cuarto)
- `position`: 'full', 'top', 'bottom', 'left', 'right', 'top-left', etc.
- `display`: objeto de monitor Electron

Calcula:
- `x`, `y`: coordenadas esquina superior-izquierda
- `width`, `height`: dimensiones de ventana

**Ejemplo - Pantalla completa (1/1)**:

```
Monitor: 1920x1080
┌────────────────────────────────────┐
│                                    │
│  x: 0                              │
│  y: 0                              │
│  width: 1920                        │
│  height: 1080                       │
│                                    │
└────────────────────────────────────┘
```

**Ejemplo - Mitad izquierda (1/2 left)**:

```
Monitor: 1920x1080
┌──────────────────────────────────────┐
│  x: 0                  │            │
│  y: 0                  │            │
│  width: 960            │   (resto)  │
│  height: 1080          │            │
│                        │            │
└────────────────────────────────────┘
```

**Ejemplo - Cuarto superior-izquierdo (1/4 top-left)**:

```
Monitor: 1920x1080
┌────────────────────┬────────────────┐
│  x: 0    │ (otro)  │                │
│  y: 0    │         │                │
│  width: 960        │ (otros cuartos)│
│  height: 540       │                │
├────────────────────┼────────────────┤
│                    │                │
└────────────────────┴────────────────┘
```

**Soporte multi-monitor**:

```javascript
const { screen } = require('electron');

// Obtiene todos los monitores
const displays = screen.getAllDisplays();

// Ordena por posición x,y
// Identifica monitor "activo" (donde estará ventana)

// Retorna posición relativa a ESE monitor, no al virtuales 0,0
```

---

### 7. **inactivityManager.js** - Temporizador de Inactividad

**Responsabilidad**: Detectar inactividad del usuario y resetear configuración automáticamente.

**¿Qué es inactividad?**

Usuario no interactúa por `config.inactivityTimeMs` (generalmente 3000ms = 3 segundos)

**Flujo**:

```
1. Usuario realiza acción (click, keypress, etc.)
   ↓
2. evento 'reset-inactivity-timer' enviado via IPC
   ↓
3. inactivityManager cancela setTimeout anterior
   ↓
4. inactivityManager inicia NUEVO setTimeout
   ↓
5. Espera 3 segundos...
   ├─ Si hay actividad: reinicia (paso 3)
   └─ Si no hay actividad: timeout dispara
       ↓
       6. Cierra todas las ventanas
       ↓
       7. Abre selector nuevamente
       ↓
       8. Usuario debe elegir configuración nuevamente
```

**Implementación**:

```javascript
function resetInactivityTimer() {
    // Cancelar timer anterior si existe
    if (appState.inactivityTimer) {
        clearTimeout(appState.inactivityTimer);
    }
    
    // Crear nuevo timer
    appState.inactivityTimer = setTimeout(() => {
        // Timeout disparado - resetear app
        closeAllWindows();
        createSelectorWindow();
    }, config.inactivityTimeMs);
}
```

**¿Cuándo se resetea el timer?**

Desde el renderizado (index.html):

```javascript
// Cada vez que usuario interactúa
document.addEventListener('click', () => {
    window.api.resetInactivityTimer();  // Envía IPC
});

document.addEventListener('keypress', () => {
    window.api.resetInactivityTimer();  // Envía IPC
});
```

---

### 8. **ipcHandlers.js** - Comunicación Inter-Proceso

**Responsabilidad**: Registrar todos los manejadores de eventos IPC que comunican main ↔ renderer.

**Tipos de comunicación IPC**:

1. **Main → Renderer** (invokeHandlers):
   Envía datos desde proceso principal a ventana renderizada
   ```javascript
   ipcMain.handle('get-config', async () => {
       return configManager.getConfig();
   });
   ```

2. **Renderer → Main** (invoke):
   Ventana solicita datos al proceso principal
   ```javascript
   const config = await window.api.getConfig();
   ```

3. **Main ← Renderer** (on/emit):
   Proceso principal escucha eventos de ventana
   ```javascript
   ipcMain.on('selection-made', (event, config) => {
       // Usuario eligió configuración en selector
       createMainWindow(config);
   });
   ```

**Manejadores registrados**:

```javascript
registerHandlers() {
    // Cuando selector envía: usuario eligió tamaño
    ipcMain.on('selection-made', (event, { size, position }) => {
        // Crear ventanas con esa configuración
    });
    
    // Cuando renderer envía: reset inactividad
    ipcMain.on('reset-inactivity-timer', () => {
        inactivityManager.resetTimer();
    });
    
    // Renderer solicita: obtener configuración
    ipcMain.handle('get-config', async () => {
        return configManager.getConfig();
    });
    
    // ... más manejadores
}
```

**Seguridad**:
- Usar `ipcMain.handle()` (2 vías) es más seguro que `ipcMain.on()` (1 vía)
- Validar siempre datos recibidos del renderer
- Usar preload.js para exponer solo API permitida

---

### 9. **preload.js** - API Segura para Renderers

**Responsabilidad**: Exponer solo funciones permitidas del main process al renderer.

**¿Por qué es necesario?**

Sin preload.js:
- Renderer tendría acceso a `require()` y Node.js completo
- Riesgo de seguridad crítico (acceso a archivos, red, etc.)
- Un hack en renderer = acceso total al sistema

Con preload.js:
- Renderer solo puede llamar funciones EXPLÍCITAMENTE permitidas
- Aislamiento de contexto (contextIsolation: true)
- Seguridad de caja de arena (sandbox: true)

**Implementación**:

```javascript
// JavaScript/preload.js

const { contextBridge, ipcRenderer } = require('electron');

// Exponer API segura SOLO en window.api
contextBridge.exposeInMainWorld('api', {
    
    // Llamadas que renderer PUEDE hacer:
    
    resetInactivityTimer: () => {
        ipcRenderer.send('reset-inactivity-timer');
    },
    
    sendSelection: (size, position) => {
        ipcRenderer.send('selection-made', { size, position });
    },
    
    getConfig: async () => {
        return await ipcRenderer.invoke('get-config');
    },
    
    // Lo que NO está aquí, renderer NO puede hacer
});
```

**Uso en renderer (index.html)**:

```javascript
// En index.html podemos hacer:
window.api.resetInactivityTimer();    // ✓ Permitido
await window.api.getConfig();         // ✓ Permitido

// Pero NO podemos hacer:
window.require('fs').readFileSync()  // ✗ No existe
require('child_process').exec()      // ✗ No existe
const fs = require('fs')             // ✗ require no existe

// Acceso directo bloqueado por contextIsolation
process.on(...)                      // ✗ No existe
```

---

### 10. **logManager.js** - Sistema de Logging

**Responsabilidad**: Registrar eventos, errores y debug en archivos con rotación automática.

**¿Por qué logging?**

- **Debug en producción**: Usuarios ejecutan .EXE, no vemos consola
- **Auditoría**: Saber qué pasó y cuándo
- **Diagnóstico**: Entender causas de errores

**Niveles de logging**:

```javascript
logManager.log('INFO', 'INIT', 'Aplicación iniciada');
logManager.log('WARN', 'CONFIG', 'Archivo config.json no encontrado, usando default');
logManager.log('ERROR', 'WINDOW', 'No se pudo crear ventana principal');
logManager.log('DEBUG', 'IPC', 'Evento selection-made recibido');
logManager.logFatal('CRASH', error);  // Error crítico + stack trace
```

**Formato de log**:

```
[2024-01-15 14:32:45.123] [INFO] [INIT] Aplicación iniciada.
[2024-01-15 14:32:45.456] [DEBUG] [CONFIG] Cargando config.json...
[2024-01-15 14:32:46.789] [ERROR] [WINDOW] No se pudo crear ventana: ENOENT
```

**Rotación automática**:

- Cada log en archivo separado por día: `log_2024-01-15.txt`
- Si archivo supera límite de tamaño → nuevo archivo
- Logs antiguos se conservan (historiales)
- En carpeta: `config.logFilePath` (ej: `C:\recursos\log\`)

**Ubicación en AppData**:

```
C:\Users\Usuario\AppData\Roaming\AppName\
├── config.json          # Configuración persistente
├── logs/
│   ├── log_2024-01-15.txt
│   ├── log_2024-01-14.txt
│   └── log_2024-01-13.txt
```

---

## ⚙️ Configuración

### config.json

Archivo de configuración centralizado con todos los parámetros del sistema.

```json
{
  "logFilePath": "C:\\recursos\\log",
  "resourcesDir": "C:\\recursos",
  "inactivityTimeMs": 3000,
  "htmlDirName": "html",
  "imageDirName": "imagenes",
  "userFileName": "contenido.txt",
  "bannersTopDirName": "BannersTop",
  "bannersBottomDirName": "BannersBottom",
  "mobileImgsDirName": "Moviles",
  "iconPath": "imagenes/icon/icon.png"
}
```

**Explicación DETALLADA de cada parámetro**:

#### 1. `logFilePath` (string)
**¿Qué es?** Directorio donde la aplicación guarda todos los archivos de logging.

**Valor actual:**
```json
"logFilePath": "C:\\recursos\\log"
```

**¿Qué hace?**
- La aplicación registra cada evento, error y debug en archivos .txt
- Estos archivos se guardan en `C:\recursos\log\`
- Se crean archivos diarios: `log_2024-01-15.txt`, `log_2024-01-14.txt`, etc.
- Permiten debugging cuando la app está en .EXE (usuarios no ven consola)

**Ejemplo de contenido**:
```
[2024-01-15 14:32:45.123] [INFO] [INIT] Aplicación iniciada.
[2024-01-15 14:32:46.456] [DEBUG] [WINDOW] Ventana creada en posición (0,0)
[2024-01-15 14:32:47.789] [ERROR] [IPC] Error comunicación con renderer
```

**Cambiar ubicación**:
```json
"logFilePath": "D:\\Logs\\MyApp"     // Otra unidad
"logFilePath": "C:\\temp\\app-logs"  // Carpeta temporal
```

---

#### 2. `resourcesDir` (string)
**¿Qué es?** Directorio raíz donde están TODOS los recursos de la aplicación.

**Valor actual:**
```json
"resourcesDir": "C:\\recursos"
```

**¿Qué contiene?**
```
C:\recursos\
├── log/                    # Logs (especificado en logFilePath)
├── imagenes/               # Imágenes, iconos, fondos
├── BannersTop/             # Banners parte superior
├── BannersBottom/          # Banners parte inferior
├── Moviles/                # Imágenes móviles
├── videos/                 # Videos (si hay)
└── contenido.txt           # Archivo de contenido
```

**¿Por qué es importante?**
- Es la carpeta "raíz" de donde se lee TODO
- Todas las rutas relativas se calculan desde aquí
- Facilita cambiar ubicación completa sin editar código

**Cambiar ubicación**:
```json
"resourcesDir": "D:\\AppContent"     // En otra unidad
"resourcesDir": "E:\\MediaLibrary"   // Servidor de contenido
```

**En código** (cómo se usa):
```javascript
const config = configManager.getConfig();
const imagePath = path.join(config.resourcesDir, config.imageDirName, 'background.jpg');
// Resultado: C:\recursos\imagenes\background.jpg
```

---

#### 3. `inactivityTimeMs` (number)
**¿Qué es?** Tiempo en milisegundos que espera sin actividad del usuario antes de resetear.

**Valor actual:**
```json
"inactivityTimeMs": 3000
```

**¿Qué significa?**
- `3000` = 3000 milisegundos = 3 segundos
- Si el usuario NO interactúa por 3 segundos → la app se resetea
- Se cierra la ventana principal y reabre el selector

**Cronograma**:
```
T=0s: Usuario hace click
  └─ Timer inicia: conteo 0→1→2→3 segundos

T=1s: Usuario sigue inactivo
  └─ Timer continúa: 1→2→3 segundos

T=2.5s: Usuario hace click nuevamente
  └─ ¡Timer se CANCELA y reinicia desde 0!
  └─ Nuevo conteo: 0→1→2→3 segundos

T=5.5s: Aún inactivo, timer alcanza 3s
  └─ ¡TIMEOUT DISPARA!
  └─ Cierra ventana
  └─ Abre selector nuevamente
```

**Cambiar tiempo**:

```json
"inactivityTimeMs": 1000      // 1 segundo (muy corto)
"inactivityTimeMs": 5000      // 5 segundos (moderado)
"inactivityTimeMs": 10000     // 10 segundos (largo)
"inactivityTimeMs": 30000     // 30 segundos (para testing)
"inactivityTimeMs": 60000     // 1 minuto (muy largo)
```

**Casos de uso**:
- Kiosco público: 3-5 segundos (rápido reset)
- Tienda digital: 10-15 segundos (da tiempo de lectura)
- Oficina: 30-60 segundos (trabajo más largo)

---

#### 4. `htmlDirName` (string)
**¿Qué es?** Nombre de la CARPETA que contiene los archivos HTML (interfaz).

**Valor actual:**
```json
"htmlDirName": "html"
```

**¿Qué contiene?**
```
html/                  (la carpeta)
├── selector.html      # Ventana de selección inicial
├── index.html         # Ventana principal de contenido
└── background.html    # Ventana de fondo
```

**¿Cómo se usa en código?**
```javascript
// En pathManager.js:
const pathManager = {
    selectorHtml: path.join(__dirname, '..', config.htmlDirName, 'selector.html'),
    // Resultado: C:\app\html\selector.html
    
    mainHtml: path.join(__dirname, '..', config.htmlDirName, 'index.html'),
    // Resultado: C:\app\html\index.html
};
```

**Cambiar nombre**:
```json
"htmlDirName": "views"          // Si la carpeta se llama "views"
"htmlDirName": "ui"             // Si se llama "ui"
"htmlDirName": "interfaces"     // Nombre descriptivo
```

⚠️ **IMPORTANTE**: Debe coincidir con el nombre real de la carpeta.

---

#### 5. `imageDirName` (string)
**¿Qué es?** Nombre de la carpeta de imágenes de la APLICACIÓN (iconos, UI).

**Valor actual:**
```json
"imageDirName": "imagenes"
```

**¿Qué contiene?**
```
imagenes/
├── icon/
│   ├── icon.png       # Icono para ventanas
│   ├── icon.ico       # Icono para Windows .exe
│   └── icon.icns      # Icono para macOS
├── logo.png           # Logo de la app
├── bg-default.jpg     # Fondo por defecto
└── ui-elements/       # Elementos de interfaz
```

**¿Para qué se usa?**
- **Icono de la aplicación** (barra de titulo, taskbar)
- **Logos** mostrados en ventanas
- **Elementos visuales** de la interfaz

**Ruta completa**:
```
C:\recursos\imagenes\  (resourcesDir + imageDirName)
```

**Cambiar nombre**:
```json
"imageDirName": "assets"         // Nombre común
"imageDirName": "img"            # Abreviado
"imageDirName": "graphics"       # Descriptivo
```

---

#### 6. `userFileName` (string)
**¿Qué es?** Nombre del archivo donde se guarda contenido del usuario.

**Valor actual:**
```json
"userFileName": "contenido.txt"
```

**¿Qué contiene?**
```
C:\recursos\contenido.txt

Ejemplo de contenido:
---
Esto es contenido personalizado
que el usuario puede editar
```

**¿Para qué sirve?**
- Guardar texto/contenido que el usuario escribe en la aplicación
- Persistencia entre sesiones (cuando cierra y reabre)
- Cargar contenido predefinido al iniciar

**Cambiar nombre**:
```json
"userFileName": "datos.txt"      // Nombre genérico
"userFileName": "contenido.md"   # Markdown
"userFileName": "config.txt"     # Para configuración
```

**En código** (cómo se carga):
```javascript
const config = configManager.getConfig();
const contentPath = path.join(config.resourcesDir, config.userFileName);
const content = fs.readFileSync(contentPath, 'utf-8');
console.log(content);  // Mostrar en app
```

---

#### 7. `bannersTopDirName` (string)
**¿Qué es?** Nombre de la carpeta de banners que aparecen en la PARTE SUPERIOR.

**Valor actual:**
```json
"bannersTopDirName": "BannersTop"
```

**¿Qué contiene?**
```
BannersTop/
├── banner1.jpg       # Banner 1920x200px
├── banner2.png       # Banner para pantalla completa
├── promotional.jpg   # Contenido promocional
└── ads.jpg          # Publicidad
```

**Ubicación**:
```
C:\recursos\BannersTop\  (resourcesDir + bannersTopDirName)
```

**Visualización en la aplicación**:
```
┌─────────────────────────────────────┐
│  BANNER DE ARRIBA (index.html)      │  ← De aquí
├─────────────────────────────────────┤
│                                     │
│  Contenido principal                │
│  (Videos, texto, imágenes)          │
│                                     │
├─────────────────────────────────────┤
│  Banner de abajo                    │  ← De bannersBottomDirName
└─────────────────────────────────────┘
```

**Cambiar nombre**:
```json
"bannersTopDirName": "HeaderBanners"   # En inglés
"bannersTopDirName": "Superior"        # Descriptivo
"bannersTopDirName": "TopAds"         # Publicidad superior
```

---

#### 8. `bannersBottomDirName` (string)
**¿Qué es?** Nombre de la carpeta de banners que aparecen en la PARTE INFERIOR.

**Valor actual:**
```json
"bannersBottomDirName": "BannersBottom"
```

**¿Qué contiene?**
```
BannersBottom/
├── footer-banner.jpg      # Banner pie de página
├── info-bar.png           # Barra informativa
├── qr-code-zone.jpg       # Código QR
└── contact-info.jpg       # Información de contacto
```

**Ubicación**:
```
C:\recursos\BannersBottom\  (resourcesDir + bannersBottomDirName)
```

**Visualización**:
```
┌─────────────────────────────────────┐
│  Banner arriba (BannersTopDirName)  │
├─────────────────────────────────────┤
│                                     │
│  Contenido principal                │
│                                     │
├─────────────────────────────────────┤
│  BANNER DE ABAJO (index.html)       │  ← De aquí
└─────────────────────────────────────┘
```

**Cambiar nombre**:
```json
"bannersBottomDirName": "FooterBanners"  # Pie de página
"bannersBottomDirName": "Inferior"       # Descriptivo
"bannersBottomDirName": "BottomAds"     # Publicidad inferior
```

---

#### 9. `mobileImgsDirName` (string)
**¿Qué es?** Nombre de la carpeta de imágenes OPTIMIZADAS PARA MÓVILES.

**Valor actual:**
```json
"mobileImgsDirName": "Moviles"
```

**¿Qué contiene?**
```
Moviles/
├── smartphone-bg.jpg       # Fondo para teléfono
├── tablet-layout.png       # Layout para tablet
├── responsive-images/      # Imágenes adaptables
└── small-resolution/       # Baja resolución (datos móviles lentos)
```

**¿Por qué existe?**
- Si la app se usa también en tablets/teléfonos
- Las imágenes móviles son más pequeñas (menos bytes)
- Carga más rápido en conexiones lentas
- Evita descargar imágenes full-HD innecesariamente

**Ubicación**:
```
C:\recursos\Moviles\  (resourcesDir + mobileImgsDirName)
```

**Comparación**:
```
Imágenes Desktop:           Imágenes Móviles:
imagenes/bg-4k.jpg (8MB)    Moviles/bg-mobile.jpg (500KB)
imagenes/banner.png (2MB)   Moviles/banner-sm.png (200KB)
```

**Cambiar nombre**:
```json
"mobileImgsDirName": "Mobile"         # En inglés
"mobileImgsDirName": "Responsive"     # Responsivo
"mobileImgsDirName": "Tablets"        # Si solo tablets
```

---

#### 10. `iconPath` (string)
**¿Qué es?** Ruta del icono de la APLICACIÓN (el que sale en barra de titulo, taskbar).

**Valor actual:**
```json
"iconPath": "imagenes/icon/icon.png"
```

**¿Qué es?**
- Imagen del icono que representa la aplicación
- Sale en:
  - Barra de titulo de ventanas
  - Taskbar de Windows
  - Dock de macOS
  - Shortcuts del escritorio
  - Instalador (.exe)

**Ruta completa interpretada**:
```
Base:           C:\recursos\             (resourcesDir)
+ iconPath:     imagenes/icon/icon.png
= Completa:     C:\recursos\imagenes\icon\icon.png
```

**¿Por qué es relativa?**
- Funciona igual en desarrollo y producción
- No depende de la unidad (C:, D:, etc.)
- Portable entre PCs

**Archivos necesarios**:

| Extensión | Sistema | Dónde sale |
|-----------|---------|-----------|
| `.png` | Todos | Windows/Mac/Linux (desarrollo) |
| `.ico` | Windows | Barra titulo, taskbar |
| `.icns` | macOS | Dock, Finder |
| `.svg` | Linux | Gestor de ventanas |

**Carpeta típica**:
```
imagenes/icon/
├── icon.png       # 256x256 (desarrollo)
├── icon.ico       # 256x256 (Windows .exe)
├── icon.icns      # 512x512 (macOS .dmg)
└── icon.svg       # Vectorial (Linux)
```

**Cambiar ruta**:
```json
"iconPath": "assets/logo.png"          # Otra carpeta
"iconPath": "img/app-icon.png"        # Nombre diferente
"iconPath": "../../shared-icons/app.ico"  # Carpeta compartida
```

---

### 📊 Estructura Completa de Carpetas

Cómo quedaría la estructura según config.json:

```
C:\recursos\                          (resourcesDir)
│
├── log/                              (logFilePath)
│   ├── log_2024-01-15.txt
│   ├── log_2024-01-14.txt
│   └── ...
│
├── imagenes/                         (imageDirName)
│   ├── icon/
│   │   ├── icon.png                  (iconPath)
│   │   ├── icon.ico
│   │   └── icon.icns
│   ├── logo.png
│   └── backgrounds/
│
├── BannersTop/                       (bannersTopDirName)
│   ├── banner1.jpg
│   ├── banner2.jpg
│   └── promotional.jpg
│
├── BannersBottom/                    (bannersBottomDirName)
│   ├── footer.jpg
│   ├── contact.jpg
│   └── qr-code.png
│
├── Moviles/                          (mobileImgsDirName)
│   ├── smartphone-bg.jpg
│   ├── tablet-layout.png
│   └── responsive/
│
└── contenido.txt                     (userFileName)
```

---

### 🔄 Cómo Se Usan Juntos

**Ejemplo práctico**: Cargar un banner al iniciar

```javascript
const config = configManager.getConfig();

// 1. Construir ruta al banner superior
const bannerTop = path.join(
    config.resourcesDir,           // C:\recursos
    config.bannersTopDirName,      // BannersTop
    'principal.jpg'                // archivo
);
// Resultado: C:\recursos\BannersTop\principal.jpg

// 2. Construir ruta al banner inferior
const bannerBottom = path.join(
    config.resourcesDir,           // C:\recursos
    config.bannersBottomDirName,   // BannersBottom
    'footer.jpg'
);
// Resultado: C:\recursos\BannersBottom\footer.jpg

// 3. Cargar contenido del usuario
const userContent = path.join(
    config.resourcesDir,           // C:\recursos
    config.userFileName            // contenido.txt
);
// Resultado: C:\recursos\contenido.txt
const content = fs.readFileSync(userContent, 'utf-8');

// 4. Esperar a inactividad
setTimeout(() => {
    logManager.log('INFO', 'INACTIVITY', 'Usuario inactivo 3s');
}, config.inactivityTimeMs);  // 3000ms
```

---

### 💡 Tips de Configuración

**Para kiosco rápido** (reset cada 3s):
```json
"inactivityTimeMs": 3000
```

**Para tienda/galería** (más tiempo de exploración):
```json
"inactivityTimeMs": 15000
```

**Para testing** (debugging con mucho tiempo):
```json
"inactivityTimeMs": 120000
```

**Usar carpetas externas** (no en recursos):
```json
"logFilePath": "D:\\Logs\\MyApp",
"resourcesDir": "E:\\MediaServer\\AppContent"
```

**Para multi-idioma** (agregar banners por idioma):
```
BannersTop/
├── es/
│   └── promo-es.jpg
└── en/
    └── promo-en.jpg
```

Luego en código:
```javascript
const lang = getUserLanguage();
const banner = path.join(config.resourcesDir, config.bannersTopDirName, lang, 'promo.jpg');
```

**¿Dónde se guarda?**

1. **Modo desarrollo**: Junto a main.js (`config/config.json`)
2. **Modo producción**: `C:\Users\Usuario\AppData\Roaming\AppName\config.json`

**¿Cómo modificarlo?**

```powershell
# Editar directamente
notepad "C:\Users\Usuario\AppData\Roaming\Interactive-Content-Editor\config.json"

# O programáticamente
const configManager = require('./configManager');
const config = configManager.getConfig();
config.inactivityTimeMs = 5000;  // Cambiar a 5 segundos
configManager.saveConfig();      # Guardar cambios
```

---

## 🔄 Flujo de Ejecución

### 1️⃣ Primer Inicio (Sin sesión guardada)

```
npm start
    ↓
main.js carga
    ├─ Carga config.json
    ├─ Inicializa logManager
    ├─ Registra IPC handlers
    └─ app.whenReady()
        ├─ Intenta cargar última sesión
        ├─ No existe → createSelectorWindow()
        ↓
selector.html abre
    ├─ Usuario ve botones:
    │  ├─ "Pantalla Completa"
    │  ├─ "Mitad Izquierda"
    │  ├─ "Mitad Derecha"
    │  └─ "4 Cuartos"
    ├─ Usuario elige
    └─ IPC 'selection-made' → main.js
        ↓
        ipcHandlers.js recibe evento
        ├─ Guarda configuración con configManager.saveLastConfig()
        ├─ Calcula posiciones con positionCalculator
        ├─ Crea ventanas con windowManager
        ├─ Inicia timer inactividad con inactivityManager
        └─ Muestra index.html en ventana principal
            ↓
index.html renderizado
    ├─ Usuario interactúa (click, tecla)
    └─ Cada acción → window.api.resetInactivityTimer()
        ├─ IPC envía al main.js
        ├─ inactivityManager cancela timer anterior
        └─ Inicia nuevo timer de 3 segundos
            ├─ Si hay más actividad → reinicia timer
            └─ Si no hay actividad por 3s → timeout
                ├─ Cierra todas las ventanas
                └─ Abre selector nuevamente (vuelve al inicio)
```

### 2️⃣ Reinicio (Con sesión guardada)

```
npm start
    ↓
main.js carga
    ├─ Carga config.json
    ├─ Registra IPC handlers
    └─ app.whenReady()
        ├─ Intenta cargar última sesión
        ├─ SÍ EXISTE → Salta selector
        ├─ Emite IPC 'selection-made' internamente
        └─ Valida y crea ventanas automáticamente
            ↓
index.html abre inmediatamente
    ├─ Sin mostrar selector
    └─ Con misma configuración que última vez
```

### 3️⃣ Cierre Normal

```
Usuario cierra ventana principal
    ↓
windowManager.js maneja evento 'closed'
    ├─ Elimina referencia de appState.windows
    ├─ Si no hay más ventanas:
    │  └─ Abre selector nuevamente
    └─ Si hay más ventanas:
       └─ Sigue ejecutándose
           ↓
Usuario cierra selector (o todas las ventanas)
    ├─ appState.windows.length === 0
    ├─ app.quit()
    └─ Proceso principal termina
        ↓
logManager.log('INFO', 'APP_QUIT', 'Aplicación terminada.')
```

---

## 📦 Instalación y Uso

### Requisitos Previos

- **Node.js** v14+ (incluye npm)
- **Windows**, **macOS** o **Linux**

Verificar instalación:

```powershell
node --version    # Debe ser v14 o superior
npm --version     # Debe ser v6 o superior
```

### Instalación

1. **Clonar o descargar proyecto**:

```powershell
cd C:\Users\Daniel\Documents\GitHub\Scripts-Prueba\Interactive-Text-Editor-main\node\Prueba15
```

2. **Instalar dependencias**:

```powershell
npm install
```

Esto descargará:
- `electron` - Framework para escribir apps de escritorio
- `electron-builder` - Para compilar ejecutable

3. **Verificar instalación**:

```powershell
npm list
# Debe mostrar electron y electron-builder instalados
```

### Uso

#### Modo Desarrollo

```powershell
npm start
```

**Qué pasa:**
- Abre la aplicación en modo desarrollo
- Devtools disponibles (Ctrl+Shift+I)
- Ver logs en consola
- Cambios en archivos se reflejan al recargar (F5)

#### Construir Ejecutable

```powershell
npm run build:win
```

**Qué pasa:**
- Compila la aplicación
- Genera instalador .nsis en carpeta `dist/`
- Genera archivo .exe portátil
- Puede distribuir a usuarios

**En macOS:**

```powershell
npm run build:mac
```

Genera `.dmg` para instalar en Mac.

#### Desinstalar y Reinstalar

```powershell
# Borrar dependencias
Remove-Item -Recurse node_modules

# Borrar cache npm
npm cache clean --force

# Reinstalar
npm install
```

---

## 🎨 Interfaz de Usuario

### 1. **selector.html** - Ventana de Configuración

**Propósito**: Permitir usuario elegir tamaño y posición de ventanas.

**Elementos**:

```html
┌─────────────────────────────┐
│  Selector de Configuración  │
├─────────────────────────────┤
│                             │
│  [Pantalla Completa]        │
│  [Mitad Izquierda]          │
│  [Mitad Derecha]            │
│  [Mitad Arriba]             │
│  [Mitad Abajo]              │
│  [4 Cuartos]                │
│  [Otros layouts...]         │
│                             │
└─────────────────────────────┘
```

**Interacción**:

```javascript
// Cuando usuario hace click en un botón
button.addEventListener('click', () => {
    // Enviar evento al main process
    window.api.sendSelection('1/2', 'left');
    
    // IPC 'selection-made' en main.js
    // ↓ Crea ventanas
});
```

### 2. **index.html** - Ventana Principal

**Propósito**: Mostrar contenido principal (video, texto, imágenes).

**Elementos básicos**:

```html
┌──────────────────────────────────┐
│   Ventana Principal              │
├──────────────────────────────────┤
│                                  │
│  [Contenido del usuario]         │
│  - Videos                        │
│  - Imágenes                      │
│  - Texto                         │
│  - HTML renderizado              │
│                                  │
│  (Fondo sincronizado con bg.html)│
│                                  │
└──────────────────────────────────┘
```

**Funcionalidad**:

```javascript
// Cada interacción resetea timer de inactividad
document.addEventListener('click', () => {
    window.api.resetInactivityTimer();
});

document.addEventListener('keypress', () => {
    window.api.resetInactivityTimer();
});

// Si usuario no interactúa por 3s:
// → Ventana cierra
// → Selector reabre
```

### 3. **background.html** - Ventana de Fondo

**Propósito**: Renderizar fondos sincronizados detrás de ventana principal.

**Características**:

- Ventana invisible al usuario (detrás)
- Mismo tamaño y posición que index.html
- Renderiza fondos, patrones, videos de fondo
- Sincronizado con contenido principal

**Arquitectura**:

```
┌─────────────────────────────┐
│ Fondo (background.html)     │  ← Detrás
├─────────────────────────────┤
│ Contenido (index.html)      │  ← Encima
└─────────────────────────────┘
```

---

## 📊 Sistema de Logs

### Ubicación de Logs

```
Windows:
C:\Users\Usuario\AppData\Roaming\Interactive-Content-Editor\logs\

Mac:
~/Library/Application Support/Interactive-Content-Editor/logs/

Linux:
~/.config/Interactive-Content-Editor/logs/
```

### Estructura de Logs

```
logs/
├── log_2024-01-15.txt    # Logs de hoy
├── log_2024-01-14.txt    # Logs de ayer
├── log_2024-01-13.txt    # Logs antiguos
└── log_2024-01-12.txt
```

### Contenido de Logs

```
[2024-01-15 14:32:45.123] [INFO] [INIT] Aplicación iniciada. Flujo de logs asegurado.
[2024-01-15 14:32:45.456] [INFO] [CONFIG_LOADED] Configuración cargada. Tiempo de inactividad: 3000ms
[2024-01-15 14:32:46.789] [INFO] [INIT] Restaurando sesión: 1/2/left
[2024-01-15 14:32:47.012] [DEBUG] [IPC] Evento selection-made recibido
[2024-01-15 14:32:48.345] [INFO] [WINDOW] Ventana principal creada en posición (0, 0) con tamaño 960x1080
[2024-01-15 14:32:49.678] [DEBUG] [TIMER] Temporizador inactividad iniciado - 3000ms
[2024-01-15 14:35:52.901] [ERROR] [WINDOW] No se pudo crear ventana: ENOENT archivo no existe
[2024-01-15 14:35:53.234] [FATAL] [CRASH] Error crítico: Cannot read property 'x' of undefined
Stack trace:
    at positionCalculator.calculatePosition (positionCalculator.js:45:23)
    at createMainWindow (windowManager.js:89:45)
    ...
[2024-01-15 14:36:00.567] [INFO] [APP_QUIT] Aplicación terminada.
```

### Acceder a Logs

**En desarrollo (DevTools)**:

```powershell
npm start
# Presionar Ctrl+Shift+I
# Ver consola
```

**En producción (.EXE)**:

```powershell
# Abrir carpeta de logs
explorer "$env:APPDATA\Interactive-Content-Editor\logs"

# Ver últimos logs
Get-Content "C:\Users\Usuario\AppData\Roaming\Interactive-Content-Editor\logs\log_$(Get-Date -Format 'yyyy-MM-dd').txt" -Tail 50
```

---

## 🚀 Características Avanzadas

### Multi-monitor

La aplicación detecta automáticamente:

```javascript
const { screen } = require('electron');
const displays = screen.getAllDisplays();

// displays[0] → Monitor principal (donde está taskbar)
// displays[1] → Monitor secundario
// displays[2] → Monitor terciario
// ... (soporta 10+ monitores)
```

**Calcular posición en monitor 2**:

```javascript
const display = displays[1];  // Monitor secundario
const bounds = display.bounds;  // { x: 1920, y: 0, width: 1920, height: 1080 }

// Ventana se posiciona relativa a este monitor
// No al virtuales (0,0) del sistema
```

### Persistencia de Sesión

Automáticamente guarda última configuración:

```javascript
// Cuando usuario elige en selector
configManager.saveLastConfig({
    size: '1/2',        // Tamaño elegido
    position: 'left',   // Posición elegida
    timestamp: Date.now() // Cuándo se guardó
});

// Próximo inicio
const lastConfig = configManager.loadLastConfig();
if (lastConfig) {
    // Restaurar automáticamente sin mostrar selector
}
```

### Auto-Reset por Inactividad

Configurable en `config.json`:

```json
{
    "inactivityTimeMs": 3000    // 3 segundos
}
```

**Cambiar a 5 segundos**:

```json
{
    "inactivityTimeMs": 5000    // 5 segundos
}
```

Cada acción del usuario reinicia el contador:
- Click del mouse
- Tecla presionada
- Scroll
- Etc.

### Soporte Multiplataforma

Código funciona igual en:
- Windows 7, 8, 10, 11
- macOS 10.13+
- Linux (Ubuntu, Fedora, etc.)

Diferencias automáticamente manejadas:
- Rutas (backslash vs forward slash)
- Iconos (.ico vs .icns)
- Instaladores (.nsis vs .dmg vs .appImage)

---

## 🔧 Solución de Problemas

### 1. "Module not found: electron"

**Síntoma**:
```
Error: Cannot find module 'electron'
```

**Solución**:

```powershell
# Reinstalar dependencias
npm install

# O específicamente electron
npm install --save-dev electron
```

### 2. "Selector no aparece"

**Síntoma**:
- Aplicación abre pero no se ve selector
- Ventana en blanco

**Investigación**:

```powershell
# 1. Ver logs
explorer "$env:APPDATA\Interactive-Content-Editor\logs"

# 2. Abrir DevTools
npm start
Ctrl+Shift+I

# 3. Buscar mensajes de error en consola
```

**Causas comunes**:

| Causa | Solución |
|-------|----------|
| `selector.html` no encontrado | Verificar carpeta `html/` existe y contiene `selector.html` |
| Ruta incorrecta en `pathManager.js` | Editar `pathManager.js` y ajustar rutas |
| `config.json` corrupto | Eliminar y dejar que copie default |
| Permisos de archivo | Ejecutar como administrador |

### 3. "Ventanas mal posicionadas"

**Síntoma**:
- Ventanas fuera de pantalla
- Tamaño incorrecto
- En monitor incorrecto

**Debug**:

```javascript
// Agregar en positionCalculator.js
console.log('Monitores detectados:', displays);
console.log('Monitor activo:', display);
console.log('Posición calculada:', { x, y, width, height });
```

**Ejecutar**:

```powershell
npm start
Ctrl+Shift+I  # DevTools
# Ver logs en consola
```

### 4. "Config.json se reinicia cada vez"

**Síntoma**:
- Cambios a config.json no persisten
- Última sesión no se guarda

**Causa**:
- Archivo de configuración no es persistente (en modo dev)

**Solución**:

En producción (.EXE), config.json se guarda en:
```
C:\Users\Usuario\AppData\Roaming\AppName\config.json
```

En desarrollo, crear manualmente:
```powershell
mkdir "$env:APPDATA\Interactive-Content-Editor"
Copy-Item config\config.json "$env:APPDATA\Interactive-Content-Editor\config.json"
```

### 5. "Timer de inactividad no funciona"

**Síntoma**:
- Ventana no cierra después de inactividad
- Selector no reaparece

**Checklist**:

```javascript
// 1. Verificar que resetInactivityTimer se llama
// En index.html, buscar:
window.api.resetInactivityTimer()  // ✓ Debe estar

// 2. Verificar IPC está registrado
// En ipcHandlers.js buscar:
ipcMain.on('reset-inactivity-timer', ...)  // ✓ Debe estar

// 3. Verificar tiempo configurado
// En config.json:
"inactivityTimeMs": 3000  // ✓ Debe ser > 0

// 4. Ver logs
Get-Content "$env:APPDATA\Interactive-Content-Editor\logs\log_$(Get-Date -Format 'yyyy-MM-dd').txt"
// Buscar mensajes de TIMER
```

### 6. "Aplicación se cierra sin avisar"

**Síntoma**:
- App desaparece sin notificación

**Causas**:

| Causa | Evidencia |
|-------|-----------|
| Error crítico en main.js | Ver logs - habrá [FATAL] |
| config.json no cargable | Logs: "CONFIG FATAL ERROR" |
| Fallo al crear ventana | Logs: "No se pudo crear ventana" |

**Debug**:

```powershell
# 1. Ver último error en logs
$date = Get-Date -Format 'yyyy-MM-dd'
$logFile = "$env:APPDATA\Interactive-Content-Editor\logs\log_$date.txt"
Get-Content $logFile -Tail 100 | Select-String -Pattern "FATAL|ERROR"

# 2. Ejecutar en terminal para ver error
npm start
# No minimizar terminal - esperar a ver error

# 3. Si error aparece - anotar mensaje completo
```

### 7. "No se puede compilar a .EXE"

**Síntoma**:
```
Error: electron-builder failed
```

**Solución**:

```powershell
# 1. Limpiar caché
npm cache clean --force

# 2. Reinstalar
Remove-Item -Recurse node_modules
npm install

# 3. Intentar build
npm run build:win

# 4. Si falla, ver error completo
npm run build:win 2>&1 | Tee-Object build-error.txt
```

---

## 💻 Desarrollo y Extensión

### Agregar Nueva Funcionalidad

**Ejemplo: Agregar botón para cambiar idioma**

#### 1. Modificar `selector.html`

```html
<!-- Agregar botón en selector -->
<button id="langButton">Español / English</button>
```

#### 2. Crear módulo `languageManager.js`

```javascript
// JavaScript/languageManager.js
module.exports = {
    currentLang: 'es',
    
    setLanguage(lang) {
        this.currentLang = lang;
        console.log(`[LANG] Idioma cambiado a: ${lang}`);
    },
    
    getLanguage() {
        return this.currentLang;
    },
    
    translate(key, lang = null) {
        const language = lang || this.currentLang;
        const translations = {
            es: { hello: 'Hola', goodbye: 'Adiós' },
            en: { hello: 'Hello', goodbye: 'Goodbye' }
        };
        return translations[language]?.[key] || key;
    }
};
```

#### 3. Registrar IPC en `ipcHandlers.js`

```javascript
const languageManager = require('./languageManager');

ipcMain.on('set-language', (event, lang) => {
    languageManager.setLanguage(lang);
    logManager.log('INFO', 'LANG', `Idioma cambiado a ${lang}`);
});

ipcMain.handle('get-language', async () => {
    return languageManager.getLanguage();
});
```

#### 4. Exponer en `preload.js`

```javascript
contextBridge.exposeInMainWorld('api', {
    // ... funciones existentes ...
    
    setLanguage: (lang) => {
        ipcRenderer.send('set-language', lang);
    },
    
    getLanguage: async () => {
        return await ipcRenderer.invoke('get-language');
    }
});
```

#### 5. Usar en `selector.html`

```javascript
document.getElementById('langButton').addEventListener('click', () => {
    const newLang = window.api.getLanguage() === 'es' ? 'en' : 'es';
    window.api.setLanguage(newLang);
    alert(newLang === 'es' ? 'Idioma: Español' : 'Language: English');
});
```

### Estándar de Código

**Convenciones en este proyecto**:

1. **Modularización**:
   ```javascript
   // ✓ Bueno - módulo independiente
   module.exports = { función1, función2 };
   
   // ✗ Malo - código suelto
   global.var = ...
   ```

2. **Nombres descriptivos**:
   ```javascript
   // ✓ Bueno
   function calculateWindowPosition(size, display) { }
   
   // ✗ Malo
   function calc(s, d) { }
   ```

3. **Logging**:
   ```javascript
   // ✓ Bueno - para debug
   logManager.log('DEBUG', 'MODULE', 'Acción realizada');
   
   // ✗ Malo - difícil de rastrear
   console.log('done');
   ```

4. **IPC seguros**:
   ```javascript
   // ✓ Bueno - validar entrada
   ipcMain.on('set-config', (event, config) => {
       if (!config || typeof config !== 'object') return;
       configManager.saveConfig(config);
   });
   
   // ✗ Malo - sin validación
   ipcMain.on('set-config', (event, config) => {
       fs.writeFileSync(..., config);  // Puede crash
   });
   ```

### Testing Manual

Checklist para probar nueva función:

```markdown
[ ] Función ejecuta sin errores
[ ] Logs aparecen en DevTools (Ctrl+Shift+I)
[ ] Verificar archivos generados (logs, config.json)
[ ] Probar en múltiples monitores si es relevante
[ ] Comprobar que no afecta timer inactividad
[ ] Ejecutar: npm run build:win y probar .EXE
[ ] Revisar permisos (lectura/escritura de archivos)
```

### Debugging Avanzado

**Breakpoints en main.js**:

```powershell
# 1. Instalar node-inspector (opcional, para debugging remoto)
npm install -g node-inspector

# 2. Ejecutar con debugging
node --inspect=9229 JavaScript/main.js
```

**Chrome DevTools en main process**:

```
Abrir: chrome://inspect
Conectar a puerto 9229
Ver console de main.js
```

**Logs detallados**:

```javascript
// Agregar logging en funciones críticas
function createMainWindow(config) {
    logManager.log('DEBUG', 'WINDOW', `Creando ventana con config: ${JSON.stringify(config)}`);
    
    const position = positionCalculator.calculate(...);
    logManager.log('DEBUG', 'POSITION', `Posición calculada: x=${position.x}, y=${position.y}, w=${position.width}, h=${position.height}`);
    
    // ... resto del código
}
```

---

## 📈 Performance y Optimización

### Memory Leaks - Evitar Referencias Cíclicas

```javascript
// ✗ MALO - Referencia cíclica
appState.windows = [];
appState.windows[0].appState = appState;  // Circular reference

// ✓ BUENO - Referencias directas
appState.windows = [];
appState.windows[0] = windowObject;
```

### Eficiencia de IPC

```javascript
// ✗ MALO - Muchas llamadas IPC
for (let i = 0; i < 1000; i++) {
    window.api.sendData(data[i]);  // 1000 viajes IPC
}

// ✓ BUENO - Una sola llamada con lote
window.api.sendDataBatch(data);  // 1 viaje IPC
```

---

## 📝 Resumen General

Este proyecto demuestra una arquitectura profesional para aplicaciones Electron:

1. ✅ **Modularización**: Cada módulo con responsabilidad clara
2. ✅ **Seguridad**: Aislamiento de contexto, sandbox, preload.js
3. ✅ **Escalabilidad**: Fácil agregar nuevas funciones
4. ✅ **Mantenibilidad**: Código documentado y logging completo
5. ✅ **Robustez**: Manejo de errores, persistencia, multi-monitor
6. ✅ **UX**: Auto-restore, inactividad inteligente, selector intuitivo

**Casos de uso**:
- Digital signage (pantallas públicas)
- Kioscos interactivos
- Sistemas de monitoreo
- Aplicaciones multi-ventana

¡Cualquier pregunta, revisar los comentarios en el código de cada módulo! 🚀

