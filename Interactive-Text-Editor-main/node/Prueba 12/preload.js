const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  sendSelection: (data) => ipcRenderer.send('selection-made', data),
  onFileChange: (callback) => ipcRenderer.on('file-changed', (e, text) => callback(text)),
  onNoFile: (callback) => ipcRenderer.on('no-file', (e, data) => callback(data)),
  onLoadImages: (callback) => ipcRenderer.on('load-images', (e, data) => callback(data)),
  
  // NUEVA FUNCIÓN: Permite abrir el diálogo de selección de archivos en el proceso principal
  selectMediaDialog: (maxFiles) => ipcRenderer.invoke('open-media-dialog', maxFiles) 
});