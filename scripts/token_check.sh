#!/bin/bash
cd "$(dirname "$0")/.."
source .venv/bin/activate
set -a; source .env; set +a
resp=$(curl -s "https://graph.facebook.com/v23.0/$IG_USER_ID?fields=followers_count&access_token=$IG_ACCESS_TOKEN")
if echo "$resp" | grep -q '"error"'; then
  echo "$(date) - TOKEN ERROR: $resp" >> token_check.log
else
  echo "$(date) - OK" >> token_check.log
fi
