// Refactored entrypoint: delegates orchestration to AppController.
const { AppController } = require('./src/electron/AppController');

// Only initialize when running under Electron (not plain node sanity check)
if (process.versions && process.versions.electron) {
	const controller = new AppController();
	controller.init();
} else {
	console.log('main.js loaded outside Electron; skipping AppController init');
}
