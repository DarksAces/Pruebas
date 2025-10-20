const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  onLoadImages: (callback) => ipcRenderer.on('load-images', (event, images) => callback(images)),
  onFileChange: (callback) => ipcRenderer.on('file-changed', (event, text) => callback(text)),
  sendAutoSave: (text) => ipcRenderer.send('autosave', text) // opcional
});
