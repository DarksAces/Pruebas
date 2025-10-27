const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  onFileChange: (callback) => ipcRenderer.on('file-changed', (event, text) => callback(text))
});
