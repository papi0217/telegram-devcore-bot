#!/bin/bash

# This script runs the DevCore Telegram bot persistently.
# It will restart the bot automatically if it crashes.

# Activate the virtual environment
source venv/bin/activate

# Loop indefinitely to keep the bot running and restart on crash
while true; do
    echo "$(date): Starting DevCore Telegram Bot..."
    python3 bot.py
    echo "$(date): DevCore Telegram Bot crashed. Restarting in 5 seconds..."
    sleep 5
done
