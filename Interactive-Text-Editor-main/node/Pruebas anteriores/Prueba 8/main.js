// main.js
const { app, BrowserWindow, ipcMain, screen } = require('electron');
const path = require('path');
const fs = require('fs');

let winSelector;
let winMain;

const htmlDir = path.join(__dirname,'html');
const recursosDir = path.join(__dirname,'recursos');
const imagesDir = path.join(recursosDir,'imagenes');
const userFile = path.join(recursosDir,'contenido.txt');
const welcomeDir = path.join(imagesDir,'Bienvenida','welcome.png');
let lastUserText = null;

// Crear ventana selector
function createSelectorWindow() {
  winSelector = new BrowserWindow({
    width: 400,
    height: 300,
    frame: true,
    resizable: false,
    webPreferences: {
      preload: path.join(__dirname,'preload.js'),
      contextIsolation: true,
      nodeIntegration: false
    }
  });

  winSelector.loadFile(path.join(htmlDir,'selector.html'));
}

// Crear ventana principal
function createMainWindow(size, position) {
  // Obtener todos los displays
  const displays = screen.getAllDisplays();
  
  // Forzar el segundo monitor (índice 1)
  // Si no hay segundo monitor, usar el primario como fallback
  const selectedDisplay = displays[1] || screen.getPrimaryDisplay();
  
  const { width: sw, height: sh, x: screenX, y: screenY } = selectedDisplay.bounds;
  let width, height, x, y;

  if(size==="3"){ 
    width=sw; height=sh; x=screenX; y=screenY; 
  }
  else if(size==="2"){
    switch(position){
      case "1": x=screenX; y=screenY; width=sw/2; height=sh; break;
      case "2": x=screenX+sw/2; y=screenY; width=sw/2; height=sh; break;
      case "3": x=screenX; y=screenY; width=sw; height=sh/2; break;
      case "4": x=screenX; y=screenY+sh/2; width=sw; height=sh/2; break;
    }
  } else if(size==="1"){
    width = sw/2; height = sh/2;
    switch(position){
      case "1": x=screenX; y=screenY; break;
      case "2": x=screenX+sw/2; y=screenY; break;
      case "3": x=screenX; y=screenY+sh/2; break;
      case "4": x=screenX+sw/2; y=screenY+sh/2; break;
    }
  }

  winMain = new BrowserWindow({
    x, y, width, height,
    frame: false,
    resizable: false,
    alwaysOnTop: true,
    backgroundColor: '#1e1e1e',
    webPreferences: {
      preload: path.join(__dirname,'preload.js'),
      contextIsolation: true,
      nodeIntegration: false
    }
  });

  winMain.loadFile(path.join(htmlDir,'index.html'));

  if(winSelector){ winSelector.close(); winSelector=null; }

  winMain.webContents.on('did-finish-load', () => {
    if(fs.existsSync(userFile)){
      const initialText = fs.readFileSync(userFile,'utf-8');
      lastUserText = initialText;
      winMain.webContents.send('file-changed', initialText);
    } else {
      winMain.webContents.send('no-file',{ welcomePath:'file://'+welcomeDir });
    }

    if(fs.existsSync(imagesDir)){
      const imageFiles = fs.readdirSync(imagesDir).filter(f=>/\.(png|jpe?g|gif|webp)$/i.test(f));
      const bannersTop = imageFiles.filter(f=>f.startsWith('top_')).map(f=>'file://'+path.join(imagesDir,f));
      const bannersBottom = imageFiles.filter(f=>f.startsWith('bottom_')).map(f=>'file://'+path.join(imagesDir,f));
      const mobileImgs = fs.existsSync(userFile)? imageFiles.filter(f=>f.startsWith('mobile_')).map(f=>'file://'+path.join(imagesDir,f)) : [];
      winMain.webContents.send('load-images',{bannersTop,bannersBottom,mobileImgs});
    }
  });

  fs.watch(recursosDir,(eventType,filename)=>{
    if(filename==='contenido.txt'){
      if(fs.existsSync(userFile)){
        const text = fs.readFileSync(userFile,'utf-8');
        if(text!==lastUserText){
          lastUserText=text;
          winMain.webContents.send('file-changed',text);
        }
      } else {
        lastUserText=null;
        winMain.webContents.send('no-file',{ welcomePath:'file://'+welcomeDir });
      }
    }
  });
}

app.whenReady().then(createSelectorWindow);

ipcMain.on('selection-made',(e,{size,position})=>{
  createMainWindow(size,position);
});

app.on('window-all-closed',()=>{ if(process.platform!=='darwin') app.quit(); });