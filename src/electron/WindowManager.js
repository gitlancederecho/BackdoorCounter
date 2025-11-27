const { BrowserWindow, Menu } = require('electron');
const path = require('path');
const { pathToFileURL } = require('url');

class WindowManager {
  constructor() {
    this.window = null;
  }

  createMainWindow() {
    Menu.setApplicationMenu(null); // hide default menu
    const fileUrl = pathToFileURL(path.join(__dirname, '..', '..', 'display.html')).href;
    this.window = new BrowserWindow({
      width: 1600,
      height: 900,
      center: true,
      useContentSize: true,
      frame: true,
      titleBarStyle: 'hiddenInset',
      fullscreen: false,
      kiosk: false,
      simpleFullScreen: false,
      resizable: true,
      movable: true,
      backgroundColor: '#000',
      webPreferences: {
        contextIsolation: true
      }
    });
    this.window.loadURL(fileUrl);
    this.window.maximize();
    return this.window;
  }
}

module.exports = { WindowManager };