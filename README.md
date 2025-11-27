# BackdoorCounter – Instagram Follower Counter

A desktop (Electron + Flask) Instagram follower counter inspired by physical Smiirl devices. Provides a fullscreen, animated display with glow, pulsing Instagram-themed lights, and a digit roll animation when the countdown refresh triggers.

## Features
- Electron front-end with live reload during development.
- Flask backend proxy to Instagram Graph API v23.0.
- 40‑second follower count cache to limit API calls.
- Responsive layout using pure viewport units (vw/vh).
- Color flow & pulsing glow animations, multi-layer background light.
- Slot-machine style digit roll when countdown hits zero.
- Buildable macOS `.app` via `electron-builder`.

## Repository Layout
```
backend/                 # Python package (InstagramClient, FollowerCache, app factory)
	instagram_client.py    # API wrapper
	cache.py               # TTL cache class
	app_factory.py         # create_app() returning configured Flask app
server.py                # Legacy entry delegating to backend.create_app()
display.html             # Renderer HTML & embedded front-end logic
src/electron/            # Modular Electron main-process classes
	AppController.js       # Orchestrates Flask + window + reloader
	WindowManager.js       # BrowserWindow creation logic
	FlaskManager.js        # Spawns Python backend
	AutoReloader.js        # Simple file watcher for dev reload
main.js                  # Entry file calling AppController
assets/                  # Static images (logo, etc.)
requirements.txt         # Python backend dependencies
package.json             # Electron app scripts and build config
start-all.command        # Starts Electron (Flask auto-starts internally now)
tests/                   # Pytest suite
README.md                # This documentation
.env.example             # Sample environment variable file
```

## Prerequisites
- macOS with Python 3.12+ and Node.js 18+ (LTS or newer recommended).
- Instagram Graph API long-lived access token and user (IG Business / Creator account).

## Quick Start (Development)
```bash
# 1. Clone
git clone https://github.com/gitlancederecho/BackdoorCounter.git
cd BackdoorCounter

# 2. Python virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install backend deps
pip install -r requirements.txt

# 4. Copy and fill environment variables
cp .env.example .env
# Edit .env with your IG credentials

# 5. Install Electron deps
npm install

# 6. Start everything (script) OR run separately
./start-all.command
# OR
# Terminal A (backend): source .venv/bin/activate && python server.py
# Terminal B (electron): npm start
```
The Electron app spawns the Flask backend; if you run them separately ensure the backend listens on `127.0.0.1:5050`.

## Environment Variables (.env)
Populate these in `.env` (loaded automatically by `python-dotenv`):
```
IG_USER_ID=YOUR_IG_USER_ID
IG_ACCESS_TOKEN=YOUR_LONG_LIVED_ACCESS_TOKEN
```
Never commit real tokens. The application logs token length only for sanity.

## Caching Behavior
Implemented via the `FollowerCache` class (`backend/cache.py`). Default TTL = 40 seconds. Reuses the last good value on transient fetch errors.

## API Endpoints (Backend)
| Endpoint | Purpose |
|----------|---------|
| `GET /count` | Returns latest (possibly cached) follower count + age |
| `GET /debug` | Diagnostics: cache metadata, env summary, last error |
| `GET /healthz` | Simple liveness probe ("ok") |
| `GET /display` | Serves `display.html` (for non-Electron browser usage) |

## Building the macOS App
```bash
npm run build
```
Resulting `.app` appears under `dist/mac-arm64/` (architecture may vary). You can codesign / notarize later if distributing.

## Testing
Simple pytest tests validate health and caching logic.
```bash
source .venv/bin/activate
pytest -q
```

## Updating Dependencies
Backend: edit `requirements.txt` and re-run `pip install -r requirements.txt`.
Frontend: `npm install <pkg>` then commit updated `package-lock.json`.

## Production Notes
- Use a systemd service / launchd plist for the backend if decoupled from Electron.
- Rotate the long-lived access token before expiry; store it in a secure Secret manager.
- Consider adding exponential backoff if Instagram rate limits.
- Add telemetry / logging pipeline for error monitoring.

## Troubleshooting
| Symptom | Possible Cause | Fix |
|--------|----------------|-----|
| Counter stays 0 | Bad IG token or insufficient permissions | Regenerate token; ensure Business account | 
| Digit roll never triggers | Countdown logic not reaching zero (timing mismatch) | Confirm sync of polling interval & TTL | 
| Backend 500 errors | Network / token issue | Check `/debug` route for last_fetch_error | 
| Build fails | Missing dev deps | Run `npm install` again |

## License
MIT (add actual license file if desired)

## Acknowledgements
Inspired by Smiirl counters and Instagram’s Graph API. Animations crafted for an ambient display environment.
