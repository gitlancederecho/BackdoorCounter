#!/bin/zsh
cd "$(dirname "$0")"
source .venv/bin/activate
python3 server.py &
PID=$!

# Wait for healthz up to 10 seconds
for i in {1..20}; do
  if curl -s http://127.0.0.1:5050/healthz | grep -q ok; then
    break
  fi
  sleep 0.5
done

npm start

# Optional: keep backend alive until electron quits
wait $PID
