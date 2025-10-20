const { app, BrowserWindow } = require('electron');
const fs = require('fs');
const path = require('path');

function createWindow() {
  const win = new BrowserWindow({
    width: 800,
    height: 600,
    backgroundColor: '#1e1e1e'
  });

  // Leer el archivo contenido.txt
  const filePath = path.join(__dirname, 'contenido.txt');
  let text = '';
  try {
    text = fs.readFileSync(filePath, 'utf-8');
  } catch (err) {
    text = 'Error: no se pudo leer contenido.txt';
  }

  // Mostrar el contenido en la ventana
  win.loadURL(
    "data:text/html;charset=utf-8," +
    encodeURIComponent(
      `<pre style="color:white;font-family:Consolas;font-size:20px;">${text}</pre>`
    )
  );
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});
