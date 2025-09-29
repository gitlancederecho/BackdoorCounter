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

async function refresh() {
  const res = await fetch('/count');
  const data = await res.json();
  document.getElementById('count').textContent = data.count;

  const now = new Date();
  const up = document.getElementById('updated');
  up.textContent = `Last updated ${now.toLocaleTimeString()}`;

  const stale = data.cached_seconds != null && data.cached_seconds > 120; // 2x TTL
  document.body.style.opacity = stale ? 0.6 : 1;
}
setInterval(refresh, 15000);
refresh();
