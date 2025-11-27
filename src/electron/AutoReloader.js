const fs = require('fs');
const path = require('path');

class AutoReloader {
  constructor(window, watchFiles = []) {
    this.window = window;
    this.watchFiles = watchFiles;
    this.watchers = [];
  }

  start() {
    this.watchFiles.forEach(f => {
      try {
        const full = path.resolve(f);
        const watcher = fs.watch(full, { persistent: true }, () => {
          if (this.window && !this.window.isDestroyed()) {
            this.window.reload();
          }
        });
        this.watchers.push(watcher);
      } catch (e) {
        // ignore missing files
      }
    });
  }

  stop() {
    this.watchers.forEach(w => w.close());
    this.watchers = [];
  }
}

module.exports = { AutoReloader };