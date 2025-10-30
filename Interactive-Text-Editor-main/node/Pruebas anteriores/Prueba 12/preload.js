// preload.js

const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  sendSelection: (data) => ipcRenderer.send('selection-made', data),
  onFileChange: (callback) => ipcRenderer.on('file-changed', (e, text) => callback(text)),
  onNoFile: (callback) => ipcRenderer.on('no-file', (e, data) => callback(data)),
  onLoadImages: (callback) => ipcRenderer.on('load-images', (e, data) => callback(data)),
  // --- NUEVA API PARA RECIBIR EL TAMAÑO DE LA VENTANA ---
  onWindowSizeSelected: (callback) => ipcRenderer.on('window-size-selected', (e, data) => callback(data)),
  // --------------------------------------------------------
  
  // VUELTO A LO ORIGINAL: Solo pasa maxFiles
  selectMediaDialog: (maxFiles) => ipcRenderer.invoke('open-media-dialog', maxFiles) 
});