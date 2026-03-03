#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

echo "Setting up DevCore Telegram Bot environment..."

# Create a Python virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate the virtual environment
source venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Initializing database..."
python3 database.py

echo "Setup complete. To run the bot, use: ./run.sh"
