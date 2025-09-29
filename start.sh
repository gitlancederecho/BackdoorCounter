#!/usr/bin/env bash
cd "$HOME/Documents/BackdoorCounter"
source .venv/bin/activate
export IG_USER_ID=17841470282647564
export IG_ACCESS_TOKEN='YOUR_LONG_LIVED_TOKEN'
python3 server.py
