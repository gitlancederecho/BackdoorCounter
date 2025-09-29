#!/bin/zsh
cd "$(dirname "$0")"
[ -f .flask.pid ] && kill "$(cat .flask.pid)" 2>/dev/null && rm -f .flask.pid
# fallback: kill anything on port 5050
lsof -ti :5050 | xargs kill -9 2>/dev/null || true
pkill -f "server.py" 2>/dev/null || true
