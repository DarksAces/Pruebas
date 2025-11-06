// JavaScript/preload.js

const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  // Envia la seleccion de configuracion (con la nueva data: distributionScheme, assignmentMap)
  sendSelection: (data) => ipcRenderer.send('selection-made', data),
  
 // Handlers para la comunicacion del contenido (watcher, bienvenida, imagenes)
  onFileChange: (callback) => ipcRenderer.on('file-changed', (e, text) => callback(text)),
  onNoFile: (callback) => ipcRenderer.on('no-file', (e, data) => callback(data)),
  onLoadImages: (callback) => ipcRenderer.on('load-images', (e, data) => callback(data)),
  onWindowSizeSelected: (callback) => ipcRenderer.on('window-size-selected', (e, data) => callback(data)),

 // Dialogo de seleccion de archivos
  selectMediaDialog: (maxFiles) => ipcRenderer.invoke('open-media-dialog', maxFiles),

    // --- NUEVOS METODOS PARA EL CIERRE SEGURO ---
    
    // 1. Permite al Renderer ESCUCHAR la senal de cierre del Main (para guardar datos)
    onAppAboutToClose: (callback) => ipcRenderer.on('app-about-to-close', callback),
    
    // 2. Permite al Renderer ENVIAR la confirmacion al Main (indicando que el guardado termino)
    saveComplete: () => ipcRenderer.send('renderer-save-complete')
    // ---------------------------------------------
});