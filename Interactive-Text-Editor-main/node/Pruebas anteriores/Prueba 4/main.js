const { app, BrowserWindow } = require('electron');
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
  const dirPath = path.dirname(filePath);
  const imagesDir = path.join(__dirname, 'imagenes');

  // Vigilar la carpeta donde está el archivo
  fs.watch(dirPath, (eventType, filename) => {
    if (filename === path.basename(filePath)) {
      if (fs.existsSync(filePath)) {
        // Se creó o modificó el archivo
        const text = fs.readFileSync(filePath, 'utf-8');
        win.webContents.send('file-changed', text);
      } else {
        // Se eliminó el archivo
        win.webContents.send('file-deleted');
      }
    }
  });

  // Leer imágenes de la carpeta al cargar
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
