const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

class FlaskManager {
  constructor(options = {}) {
    this.cwd = options.cwd || process.cwd();
    this.python = options.python || path.join(this.cwd, '.venv', 'bin', 'python');
    this.script = options.script || path.join(this.cwd, 'server.py');
    this.process = null;
    this.pidFile = path.join(this.cwd, '.flask.pid');
  }

  start() {
    if (this.process) return;
    this.process = spawn(this.python, [this.script], {
      cwd: this.cwd,
      stdio: 'inherit'
    });
    fs.writeFileSync(this.pidFile, String(this.process.pid));
    this.process.on('exit', () => {
      if (fs.existsSync(this.pidFile)) fs.unlinkSync(this.pidFile);
    });
  }

  stop() {
    if (!this.process) return;
    try {
      this.process.kill();
    } catch (e) {
      // ignore
    }
    this.process = null;
    if (fs.existsSync(this.pidFile)) fs.unlinkSync(this.pidFile);
  }
}

module.exports = { FlaskManager };