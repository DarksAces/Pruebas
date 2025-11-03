// JavaScript/preload.js

/*
 * Preload script: expone una API segura (contextBridge) al renderer.
 * Solo deben exponerse las funciones mínimas necesarias para la UI. Esto evita
 * habilitar nodeIntegration en los renderers y mejora la seguridad.
 *
 * API expuesta (window.electronAPI):
 *  - sendSelection(data): envía al proceso main la selección final
 *  - selectMediaDialog(maxFiles): invoca el diálogo de selección y devuelve promesa
 *  - onFileChange(callback), onNoFile(callback), onLoadImages(callback), onWindowSizeSelected(callback)
 *
 * Nota de seguridad: todas las funciones usan ipcRenderer (invoke/send/on) y la exposición
 * se limita a callbacks y promesas; no se exponen objetos con acceso a Node.
 */

const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  // Envía la selección de configuración (con la nueva data: distributionScheme, assignmentMap)
  sendSelection: (data) => ipcRenderer.send('selection-made', data),
  
  // Handlers para la comunicación del contenido (watcher, bienvenida, imágenes)
  onFileChange: (callback) => ipcRenderer.on('file-changed', (e, text) => callback(text)),
  onNoFile: (callback) => ipcRenderer.on('no-file', (e, data) => callback(data)),
  onLoadImages: (callback) => ipcRenderer.on('load-images', (e, data) => callback(data)),
  onWindowSizeSelected: (callback) => ipcRenderer.on('window-size-selected', (e, data) => callback(data)),
  
  // Diálogo de selección de archivos (devuelve Promise<string[] | null>)
  selectMediaDialog: (maxFiles) => ipcRenderer.invoke('open-media-dialog', maxFiles) 
});