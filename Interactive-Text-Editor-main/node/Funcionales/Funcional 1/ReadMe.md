# Funcional 1 — Documentación detallada

Este documento describe en detalle los cambios y el funcionamiento de la entrega "Funcional 1" (renombrado desde "Prueba 13"). Contiene instrucciones de instalación y ejecución en Windows (PowerShell), un mapa de archivos, explicación técnica de los módulos principales (IPC, preload, cálculo de posiciones, asignación de fondos) y procedimientos de prueba y resolución de problemas.

## Objetivo de esta versión

Funcional 1 mejora la gestión de ventanas y la asignación de medios para ventanas de fondo. Sus metas son:

- Permitir selección de archivos consistente (sin bloqueos por límites no visibles).
- Sincronizar de forma fiable la posición deseada de la ventana principal entre UI y proceso principal.
- Añadir esquemas de distribución de fondos para configuraciones de 1/4, permitiendo combinaciones (p.ej. dos cuadrados fusionados y uno individual).
- Exponer una API segura desde el preload para dialogar con el proceso principal (selección de archivos, envío de selección, notificaciones de carga).

## Resumen de cambios principales

- Selector de archivos: ahora siempre abre el diálogo; cuando no hay un límite explícito, la UI pasa un límite alto (p.ej. 100) para permitir multi-selección y luego recorta la lista según sea necesario.
- Sincronización de posición: `mainPosition` es la fuente de la verdad. La UI muestra un panel de depuración que compara `posSelect.value` con `mainPosition` para detectar desincronizaciones.
- IPC y preload: `preload.js` exporta funciones seguras como `electronAPI.selectMediaDialog(maxFiles)` que invocan `ipcRenderer.invoke('open-media-dialog', maxFiles)`; `main.js` maneja ese canal.
- Distribución de fondos: nuevos esquemas para layouts de 1/4: `none`, `three_individual`, `one_big`, `two_halves`. Para layouts fusionados se usan índices internos especiales (98, 99) para distinguir bounds fusionados.

## Estructura del proyecto y descripción de archivos

Raíz del proyecto: `Funcional 1/`

- `package.json` — Dependencias y scripts (p.ej. `npm start`).
- `ReadMe.md` — Este archivo (documentación y guía completa).
- `config/config.json` — Configuración global (directorio de recursos por defecto, opciones de despliegue). Ver la sección "Configuración" para claves relevantes.

Carpeta `html/`:
- `selector.html` — Interfaz para elegir tamaño/posición, seleccionar archivos y asignarlos a las regiones. Incluye panel de depuración.
- `index.html` — Plantilla principal para la ventana del contenido (background/main window).
- `background.html` — Plantilla para ventanas de fondo que reproducen imágenes o vídeo.

Carpeta `JavaScript/`:
- `main.js` — Proceso principal de Electron. Maneja creación de ventanas, cálculos de posiciones (función `calculatePositions`), manejo de `ipcMain.handle('open-media-dialog')`, conversión de rutas y creación/arranque de ventanas de fondo.
- `preload.js` — Exposición de API segura al renderer: `electronAPI.selectMediaDialog(maxFiles)`, `electronAPI.sendSelection(...)`, y otros canales de comunicación. Implementa `ipcRenderer.invoke`/`on` según sea necesario.
- `ipcHandlers.js` — Manejadores auxiliares de IPC (puede contener lógica para eventos y respuestas entre procesos).
- `windowManager.js` — Helpers para crear y posicionar ventanas principales y de fondo.
- `positionCalculator.js` — Lógica para calcular bounds/rects según tipo de ventana (full, half, quarter) y selección de monitor.
- `pathManager.js` — Normalización de rutas y conversión a URLs (p.ej. `pathToFileURL`) para usar en `BrowserWindow`.
- `configManager.js` — Lectura y saneamiento de `config/config.json`.
- `appState.js` — Estado de la aplicación en memoria (mapas de asignación de medios, posiciones actuales, etc.).
- `inactivityManager.js` — Gestión de tiempo de inactividad si aplica.

## Configuración (config/config.json)

Archivo clave: `config/config.json`.

Claves importantes que debes revisar:

- `resourcesDir` (string): ruta por defecto para abrir el diálogo de archivos.
- `defaultMonitorIndex` (number, opcional): índice del monitor a usar cuando hay múltiples monitores; si no existe, se elige por heurística (`screen.getAllDisplays()` y preferencia por segundo monitor si hay varios).
- `defaultBackgroundStyle` (string): opciones de estilo por defecto para fondos.

Si necesitas que el diálogo abra otra carpeta por defecto, ajusta `resourcesDir`.

## Contrato (API pública entre renderer y main)

1) selectMediaDialog(maxFiles: number | undefined) => Promise<string[] | null>
   - Inputs: `maxFiles` (si es undefined, la UI puede enviar un entero grande para activar multi-selección).
   - Output: Array de rutas absolutas seleccionadas o `null` si se canceló.
   - Errores: Rechaza la promesa si hay error al abrir el diálogo.

2) sendSelection(payload: { position, distribution, userMediaMap }) => void
   - Envía la asignación final al proceso principal para crear la ventana y ventanas de fondo.

3) Eventos expuestos por preload:
   - `onFileChange` — Notifica cambios de selección en UI.
   - `onNoFile` — Notifica que no hay archivos asignados.
   - `onLoadImages` — Señal para que el main cargue/actualice las ventanas de fondo.

## Detalles técnicos importantes

- Multi-monitor: `calculatePositions()` consulta `screen.getAllDisplays()` y calcula bounds relativos al display elegido. Por defecto, si hay más de un monitor y no se indica, se elige el segundo (esto es configurable en `config.json`).
- Posiciones soportadas: `full`, `half` (left/right/top/bottom), `quarter` (indices 0..3). Para `quarter` hay distribuciones extra que permiten fusionar regiones (índices internos 98/99 para identificar regiones "fusionadas").
- Asignación de medios: `userMediaMap` es un objeto que mapea índices de región a rutas de archivo. Si se asigna un archivo "fusionado" se usan índices especiales y `main.js` produce bounds combinados.
- Rutas Windows: `main.js` normaliza rutas y las transforma a URL con `url.pathToFileURL(...)` antes de pasarlas a `BrowserWindow.loadURL`.

## Cómo ejecutar (Windows — PowerShell)

Abre PowerShell en la carpeta `Funcional 1` y ejecuta:

```powershell
# Instalar dependencias (sólo si es la primera vez)
npm install

# Ejecutar la aplicación (arranca Electron)
npm start
```

Notas:
- Para ver logs de la ventana `selector`, abre DevTools en esa ventana (Ctrl+Shift+I) o habilita la salida en la consola donde ejecutas `npm start`.