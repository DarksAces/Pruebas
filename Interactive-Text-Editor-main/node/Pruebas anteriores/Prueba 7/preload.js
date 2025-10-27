const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  onFileChange: (callback) => ipcRenderer.on('file-changed', (_, data) => callback(data)),
  onLoadImages: (callback) => ipcRenderer.on('load-images', (_, data) => callback(data)),
  onNoFile: (callback) => ipcRenderer.on('no-file', (_, data) => callback(data)) // ✅ recibe welcomePath correctamente
});
