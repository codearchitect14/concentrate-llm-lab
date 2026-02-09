#!/bin/bash
# Setup script for Concentrate API Exercise

echo "Setting up Concentrate API Exercise..."

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "Please edit .env and add your Concentrate API key"
else
    echo ".env file already exists"
fi

# Create outputs directory
mkdir -p outputs

echo "Setup complete!"
echo "To run the experiments: python scripts/run_exercise.py"

