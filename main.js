// main.js (or whatever your Electron entry file is)
const { app, BrowserWindow, Menu } = require("electron");
const path = require("path");
const { pathToFileURL } = require("url");

function createWindow() {
  // Hide the menu bar; keeps the title bar (traffic lights) visible
  Menu.setApplicationMenu(null);

  const fileUrl = pathToFileURL(path.join(__dirname, "display.html")).href;

  const win = new BrowserWindow({
    width: 1600,
    height: 900,
    center: true,
    useContentSize: true,

    // ✅ normal draggable window
    frame: true,
    titleBarStyle: "hiddenInset",

    // 🚫 no forced full screen / kiosk
    fullscreen: false,
    kiosk: false,
    simpleFullScreen: false,

    resizable: true,
    movable: true,
    alwaysOnTop: false,       // set true later if you want it to sit above everything
    backgroundColor: "#000",
    webPreferences: { contextIsolation: true }
  });

  win.loadURL(fileUrl);

  // Fill the screen but KEEP the title bar visible
  win.maximize();
}

app.whenReady().then(() => {
  createWindow();
  app.on("activate", () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on("window-all-closed", () => app.quit());
