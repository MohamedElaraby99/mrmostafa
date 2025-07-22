#!/usr/bin/python3.10

"""
WSGI configuration for PythonAnywhere deployment
This file is used by PythonAnywhere to serve the Flask application
"""

import sys
import os

# Add your project directory to the sys.path
path = '/home/tafrasystem/mysite'
if path not in sys.path:
    sys.path.append(path)

# Set environment variables
os.environ['FLASK_CONFIG'] = 'pythonanywhere'
os.environ['FLASK_APP'] = 'app.py'

# Import your Flask app
from app import app as application

# Initialize the application for production
if __name__ == "__main__":
    # This won't be called in production, but useful for testing
    application.run(debug=False) 