// JavaScript/preload.js

const { contextBridge, ipcRenderer } = require('electron');

// Exponemos una API segura llamada 'electronAPI' al objeto global 'window' del navegador.
// Esto permite que el frontend (HTML/JS) se comunique con el backend (Node.js) sin riesgos de seguridad.
contextBridge.exposeInMainWorld('electronAPI', {
  // --- COMUNICACIÓN DESDE EL RENDERER HACIA EL MAIN ---
  
  // Envía la configuración seleccionada por el usuario (distribución de pantallas, archivos, etc.)
  sendSelection: (data) => ipcRenderer.send('selection-made', data),
  
  // --- LISTENERS (Escuchas) DESDE EL MAIN HACIA EL RENDERER ---
  
  // Recibe notificaciones cuando el archivo de texto (contenido.txt) cambia
  onFileChange: (callback) => ipcRenderer.on('file-changed', (e, text) => callback(text)),
  
  // Recibe notificación cuando no existe el archivo de usuario (para mostrar bienvenida o resetear)
  onNoFile: (callback) => ipcRenderer.on('no-file', (e, data) => callback(data)),
  
  // Recibe las rutas de las imágenes/videos que deben cargarse en el DOM (banners, fondos, etc.)
  onLoadImages: (callback) => ipcRenderer.on('load-images', (e, data) => callback(data)),
  
  // Notifica al renderer qué tamaño de pantalla (1, 2, 3) se ha seleccionado para ajustar CSS
  onWindowSizeSelected: (callback) => ipcRenderer.on('window-size-selected', (e, data) => callback(data)),
  
  // --- UTILIDADES DEL SISTEMA ---
  
  // Invoca el diálogo nativo del sistema operativo para seleccionar archivos multimedia
  // Devuelve una promesa con los archivos seleccionados.
  selectMediaDialog: (maxFiles) => ipcRenderer.invoke('open-media-dialog', maxFiles),
  
  // **NUEVO:** Canal para enviar logs desde el Renderizador al Main
  // Permite que errores de JavaScript en el navegador se guarden en el archivo de log del servidor.
  sendRenderLog: (level, context, message) => ipcRenderer.send('render-log', { level, context, message })
});