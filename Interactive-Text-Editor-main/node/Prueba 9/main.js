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
  const { width: sw, height: sh } = screen.getPrimaryDisplay().bounds;
  let width, height, x, y;

  if(size==="3"){ width=sw; height=sh; x=0; y=0; }
  else if(size==="2"){
    switch(position){
      case "1": x=0; y=0; width=sw/2; height=sh; break; // MitIzq
      case "2": x=sw/2; y=0; width=sw/2; height=sh; break; // MitDer
      case "3": x=0; y=0; width=sw; height=sh/2; break; // MitSup
      case "4": x=0; y=sh/2; width=sw; height=sh/2; break; // MitInf
    }
  } else if(size==="1"){
    width = sw/2; height = sh/2;
    switch(position){
      case "1": x=0; y=0; break; // SupIzq
      case "2": x=sw/2; y=0; break; // SupDer
      case "3": x=0; y=sh/2; break; // InfIzq
      case "4": x=sw/2; y=sh/2; break; // InfDer
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
