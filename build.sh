#!/bin/bash

# Build script for Render deployment
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Creating logs directory..."
mkdir -p logs

echo "Validating configuration..."
python -c "from config.settings import validate_config; validate_config(); print('✓ Configuration validated')"

echo "Build completed successfully!"
