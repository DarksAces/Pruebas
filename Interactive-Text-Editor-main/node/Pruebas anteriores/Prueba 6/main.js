const { app, BrowserWindow } = require('electron');
const fs = require('fs');
const path = require('path');

let win;
const userFile = path.join(__dirname, 'contenido.txt');
const imagesDir = path.join(__dirname, 'imagenes');
const welcomeDir = path.join(__dirname, 'imagenes','Bienvenida', 'welcome.png');

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
    // Inicial: mostrar contenido o bienvenida
    if (fs.existsSync(userFile)) {
      const initialText = fs.readFileSync(userFile, 'utf-8');
      lastUserText = initialText;
      win.webContents.send('file-changed', initialText);
    } else {
      win.webContents.send('no-file', { welcomePath: 'file://' + welcomeDir });
    }

    // Cargar banners y móviles
    if (fs.existsSync(imagesDir)) {
      const imageFiles = fs.readdirSync(imagesDir).filter(f => /\.(png|jpe?g|gif|webp)$/i.test(f));
      const bannersTop = imageFiles.filter(f => f.startsWith('top_')).map(f => 'file://' + path.join(imagesDir, f));
      const mobileImgs = fs.existsSync(userFile)
        ? imageFiles.filter(f => f.startsWith('mobile_')).map(f => 'file://' + path.join(imagesDir, f))
        : [];
      const bannersBottom = imageFiles.filter(f => f.startsWith('bottom_')).map(f => 'file://' + path.join(imagesDir, f));

      win.webContents.send('load-images', { bannersTop, mobileImgs, bannersBottom });
    }
  });

  // Observar la carpeta para cambios en contenido.txt
  fs.watch(path.dirname(userFile), (eventType, filename) => {
    if (filename === 'contenido.txt') {
      if (fs.existsSync(userFile)) {
        const text = fs.readFileSync(userFile, 'utf-8');
        if (text !== lastUserText) {
          lastUserText = text;
          win.webContents.send('file-changed', text);
        }
      } else {
        // 💡 Si se borra, volver a mostrar bienvenida
        lastUserText = null;
        win.webContents.send('no-file', { welcomePath: 'file://' + welcomeDir });
      }
    }
  });
}

app.whenReady().then(createWindow);
app.on('window-all-closed', () => { if (process.platform !== 'darwin') app.quit(); });
