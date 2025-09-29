#!/bin/zsh
cd "$(dirname "$0")"
source .venv/bin/activate

# start flask and save pid
python3 server.py & echo $! > .flask.pid

# wait up to 10s for healthz
for i in {1..20}; do
  if curl -s http://127.0.0.1:5050/healthz | grep -q ok; then
    break
  fi
  sleep 0.5
done

# start electron (or npm start)
npm start

# when electron quits, stop flask
kill "$(cat .flask.pid)" 2>/dev/null || true
rm -f .flask.pid
