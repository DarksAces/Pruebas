// JavaScript/preload.js

const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  // Envía la selección de configuración (con la nueva data: distributionScheme, assignmentMap)
  sendSelection: (data) => ipcRenderer.send('selection-made', data),
  
  // Handlers para la comunicación del contenido (watcher, bienvenida, imágenes)
  onFileChange: (callback) => ipcRenderer.on('file-changed', (e, text) => callback(text)),
  onNoFile: (callback) => ipcRenderer.on('no-file', (e, data) => callback(data)),
  onLoadImages: (callback) => ipcRenderer.on('load-images', (e, data) => callback(data)),
  onWindowSizeSelected: (callback) => ipcRenderer.on('window-size-selected', (e, data) => callback(data)),
  
  // Diálogo de selección de archivos
  selectMediaDialog: (maxFiles) => ipcRenderer.invoke('open-media-dialog', maxFiles),

    // --- NUEVOS MÉTODOS PARA EL CIERRE SEGURO ---
    
    // 1. Permite al Renderer ESCUCHAR la señal de cierre del Main (para guardar datos)
    onAppAboutToClose: (callback) => ipcRenderer.on('app-about-to-close', callback),
    
    // 2. Permite al Renderer ENVIAR la confirmación al Main (indicando que el guardado terminó)
    saveComplete: () => ipcRenderer.send('renderer-save-complete')
    // ---------------------------------------------
});