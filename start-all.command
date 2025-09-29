#!/bin/zsh
cd "$(dirname "$0")"

# 1) Use your venv so Flask + CORS + dotenv are available
source .venv/bin/activate

# 2) Start Flask backend in the background (it will read .env automatically)
python3 server.py &

# 3) Give the server a moment to bind to 5050
sleep 1.5

# 4) Launch Electron
npm start
