#!/usr/bin/env python3
"""
Development server runner for Tafra Student Management System
This script runs the Flask app in development mode with auto-reload enabled
"""

import os
from app import app, init_db

if __name__ == '__main__':
    # Initialize database
    init_db()
    
    # Set development environment
    os.environ['FLASK_ENV'] = 'development'
    
    # Run in development mode with debug enabled
    print("🚀 Starting Tafra System in Development Mode...")
    print("📝 Auto-reload enabled - changes will be applied automatically!")
    print("🌐 Server running at: http://localhost:5000")
    print("⏹️  Press Ctrl+C to stop the server")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,           # Enable debug mode
        use_reloader=True,    # Auto-reload on file changes
        use_debugger=True,    # Enable interactive debugger
        threaded=True         # Handle multiple requests
    ) 