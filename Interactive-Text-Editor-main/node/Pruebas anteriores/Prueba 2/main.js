const { app, BrowserWindow, ipcMain } = require('electron');
const fs = require('fs');
const path = require('path');

let win;

function createWindow() {
  win = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js')
    },
    backgroundColor: '#1e1e1e'
  });

  win.loadFile('index.html');

  const filePath = path.join(__dirname, 'contenido.txt');

  // Vigilar cambios en el archivo
  fs.watch(filePath, (eventType) => {
    if (eventType === 'change') {
      const text = fs.readFileSync(filePath, 'utf-8');
      // enviar al renderer
      win.webContents.send('file-changed', text);
    }
  });
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});
