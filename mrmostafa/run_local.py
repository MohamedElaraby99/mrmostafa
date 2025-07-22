#!/usr/bin/env python3
"""
Local development runner for Tafra Student Management System
Requires Python 3.11 or higher
"""
import os
import sys

def setup_local_env():
    """Setup local development environment"""
    # Set development environment variables
    os.environ['FLASK_ENV'] = 'development'
    os.environ['SECRET_KEY'] = 'dev-secret-key-for-local-testing'
    
    # Use SQLite for local development
    if 'DATABASE_URL' not in os.environ:
        os.environ['DATABASE_URL'] = 'sqlite:///students.db'
    
    print("🔧 Local development environment configured")
    print(f"📁 Database: {os.environ.get('DATABASE_URL', 'Not set')}")
    print(f"🔑 Secret Key: {'Set' if os.environ.get('SECRET_KEY') else 'Not set'}")
    print(f"🌍 Environment: {os.environ.get('FLASK_ENV', 'Not set')}")
    print(f"🐍 Python Version: {sys.version}")

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required!")
        print(f"   Current version: {sys.version}")
        sys.exit(1)

def run_app():
    """Run the Flask application"""
    try:
        from app import app, init_db
        
        print("\n🚀 Starting Tafra Student Management System...")
        print("📊 Initializing database...")
        
        # Initialize database
        init_db()
        
        print("✅ Database initialized successfully!")
        print("👤 Default admin user: araby / 92321066")
        print("🌐 Starting server at http://127.0.0.1:5000")
        print("🛑 Press Ctrl+C to stop\n")
        
        # Run the application
        app.run(host='127.0.0.1', port=5000, debug=True)
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure you have installed all requirements:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        sys.exit(1)

if __name__ == '__main__':
    print("🎓 Tafra Student Management System - Local Development")
    print("=" * 50)
    
    check_python_version()
    setup_local_env()
    run_app() 