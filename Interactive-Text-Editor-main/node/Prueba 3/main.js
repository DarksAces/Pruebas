const { app, BrowserWindow, ipcMain } = require('electron');
const fs = require('fs');
const path = require('path');

let win;

function createWindow() {
  win = new BrowserWindow({
    width: 1000,
    height: 2000,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js')
    },
    backgroundColor: '#1e1e1e'
  });

  win.loadFile('index.html');

  const filePath = path.join(__dirname, 'contenido.txt');
  const imagesDir = path.join(__dirname, 'imagenes');

  // Vigilar cambios en el archivo
  fs.watch(filePath, (eventType) => {
    if (eventType === 'change') {
      const text = fs.readFileSync(filePath, 'utf-8');
      win.webContents.send('file-changed', text);
    }
  });

  // Leer imágenes de la carpeta
  if (fs.existsSync(imagesDir)) {
const imageFiles = fs.readdirSync(imagesDir)
  .filter(file => /\.(png|jpe?g|gif|webp)$/i.test(file))
  .map(file => 'file://' + path.join(__dirname, 'imagenes', file));

win.webContents.on('did-finish-load', () => {
  win.webContents.send('load-images', imageFiles);
});

  }
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});
