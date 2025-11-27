#!/bin/zsh
# Unified start script now that Electron main process launches Flask itself.
cd "$(dirname "$0")"
source .venv/bin/activate

echo "[start-all] Starting Electron (Flask will be spawned internally)..."
npm start

echo "[start-all] Electron exited."
