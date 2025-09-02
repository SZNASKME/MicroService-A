#!/usr/bin/env python3
"""
WSGI Entry Point for Data Analytics Microservice
This file is used by production WSGI servers like Gunicorn
"""

import os
import sys
from pathlib import Path

# Add the application directory to Python path
app_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(app_dir))

# Set default environment
os.environ.setdefault('FLASK_ENV', 'production')

# Import the application
from app import create_app

# Create the application instance
application = create_app()

if __name__ == "__main__":
    # This allows running with python wsgi.py for development
    application.run(
        host=os.getenv('HOST', '0.0.0.0'),
        port=int(os.getenv('PORT', 5000)),
        debug=False
    )
