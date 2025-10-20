const { app, BrowserWindow, ipcMain } = require('electron');
const fs = require('fs');
const path = require('path');

let win;
const userFile = path.join(__dirname, 'contenido.txt'); // archivo externo
const imagesDir = path.join(__dirname, 'imagenes');

let lastUserText = null;

function createWindow() {
  win = new BrowserWindow({
    width: 800,
    height: 600,
    resizable: false,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false
    },
    backgroundColor: '#1e1e1e'
  });

  win.loadFile('index.html').then(() => {
    if (fs.existsSync(userFile)) {
      const initialText = fs.readFileSync(userFile, 'utf-8');
      lastUserText = initialText;
      win.webContents.send('file-changed', initialText);
    }

    if (fs.existsSync(imagesDir)) {
      const imageFiles = fs.readdirSync(imagesDir).filter(f => /\.(png|jpe?g|gif|webp)$/i.test(f));
      const bannersTop = imageFiles.filter(f => f.startsWith('top_')).map(f => 'file://' + path.join(imagesDir, f));
      const mobileImgs = imageFiles.filter(f => f.startsWith('mobile_')).map(f => 'file://' + path.join(imagesDir, f));
      const bannersBottom = imageFiles.filter(f => f.startsWith('bottom_')).map(f => 'file://' + path.join(imagesDir, f));
      win.webContents.send('load-images', { bannersTop, mobileImgs, bannersBottom });
    }
  });

  fs.watch(userFile, (eventType) => {
    if (eventType === 'change' && fs.existsSync(userFile)) {
      const text = fs.readFileSync(userFile, 'utf-8');
      if (text !== lastUserText) {
        lastUserText = text;
        if (win) win.webContents.send('file-changed', text);
      }
    }
  });
}

app.whenReady().then(createWindow);
app.on('window-all-closed', () => { if (process.platform !== 'darwin') app.quit(); });
