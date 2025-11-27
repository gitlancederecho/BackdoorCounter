const { app } = require('electron');
const path = require('path');
const { WindowManager } = require('./WindowManager');
const { FlaskManager } = require('./FlaskManager');
const { AutoReloader } = require('./AutoReloader');

class AppController {
  constructor() {
    this.windowManager = new WindowManager();
    this.flask = new FlaskManager({ cwd: process.cwd() });
    this.reloader = null;
  }

  init() {
    app.whenReady().then(() => {
      this.flask.start();
      const win = this.windowManager.createMainWindow();
      this.reloader = new AutoReloader(win, [
        path.join(process.cwd(), 'display.html'),
        path.join(process.cwd(), 'assets', 'backdoor-logo.png')
      ]);
      this.reloader.start();

      app.on('activate', () => {
        if (this.windowManager.window === null || this.windowManager.window.isDestroyed()) {
          this.windowManager.createMainWindow();
        }
      });
    });

    app.on('window-all-closed', () => {
      this.shutdown();
    });
  }

  shutdown() {
    if (process.platform !== 'darwin') {
      app.quit();
    }
    if (this.reloader) this.reloader.stop();
    this.flask.stop();
  }
}

module.exports = { AppController };