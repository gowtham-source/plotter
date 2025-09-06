#!/bin/bash

# Setup script for Telegram Plotting Bot

echo "Setting up Telegram Plotting Bot..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "Please edit the .env file and add your Telegram Bot Token."
fi

# Create logs directory if it doesn't exist
if [ ! -d logs ]; then
    echo "Creating logs directory..."
    mkdir -p logs
fi

echo "Setup complete! You can now build and run the bot using Docker."
echo "Run 'docker-compose up -d' to start the bot."