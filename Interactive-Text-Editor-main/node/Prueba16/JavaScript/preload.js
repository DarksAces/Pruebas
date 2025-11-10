const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  // --- Comunicación general ---
  onFileChange: (callback) => ipcRenderer.on('file-changed', (e, text) => callback(text)),
  onNoFile: (callback) => ipcRenderer.on('no-file', (e, data) => callback(data)),
  onLoadImages: (callback) => ipcRenderer.on('load-images', (e, data) => callback(data)),
  onWindowSizeSelected: (callback) => ipcRenderer.on('window-size-selected', (e, data) => callback(data)),

  // --- Diálogo de selección de archivos ---
  selectMediaDialog: (maxFiles) => ipcRenderer.invoke('open-media-dialog', maxFiles),

  // --- Envío de selección al proceso principal (¡la clave que faltaba!) ---
  sendSelection: (data) => ipcRenderer.send('selection-made', data),

  // --- Texto de fondo ---
  onBackgroundTextChange: (callback) => ipcRenderer.on('background-text-changed', (e, text) => callback(text)),
  onBackgroundNoFile: (callback) => ipcRenderer.on('background-no-file', (e) => callback()),

  // --- Cierre seguro ---
  onAppAboutToClose: (callback) => ipcRenderer.on('app-about-to-close', callback),
  saveComplete: () => ipcRenderer.send('save-complete'),
});
