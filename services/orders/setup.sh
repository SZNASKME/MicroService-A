#!/bin/bash

# Setup script for Data Analytics Microservice

echo "Setting up Data Analytics Microservice..."

# Create virtual environment
echo "Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

# Create necessary directories
echo "Creating necessary directories..."
mkdir -p uploads
mkdir -p logs
mkdir -p temp
mkdir -p reports

echo "Setup completed successfully!"
echo ""
echo "To run the service:"
echo "1. Activate virtual environment:"
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    echo "   source venv/Scripts/activate"
else
    echo "   source venv/bin/activate"
fi
echo "2. Run the application:"
echo "   python app.py"
echo ""
echo "The service will be available at: http://localhost:5000"
