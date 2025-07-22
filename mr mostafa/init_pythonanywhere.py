#!/usr/bin/env python3
"""
PythonAnywhere Initialization Script
This script initializes the database and creates the default admin user for production
Run this script once after deploying to PythonAnywhere
"""

import os
import sys

# Add the project directory to Python path
project_dir = '/home/yourusername/mysite'  # Change 'yourusername' to your actual username
if project_dir not in sys.path:
    sys.path.insert(0, project_dir)

# Set environment for PythonAnywhere
os.environ['FLASK_CONFIG'] = 'pythonanywhere'

from app import app, db, create_default_admin
from datetime import datetime

def initialize_database():
    """Initialize the database for PythonAnywhere production"""
    print("🚀 Initializing Tafra Student Management System for PythonAnywhere...")
    print(f"📍 Database path: {app.config['SQLALCHEMY_DATABASE_URI']}")
    
    with app.app_context():
        try:
            # Create all database tables
            print("📊 Creating database tables...")
            db.create_all()
            print("✅ Database tables created successfully!")
            
            # Create default admin user
            print("👤 Creating default admin user...")
            create_default_admin()
            print("✅ Default admin user created!")
            
            # Print success message
            print("\n" + "="*50)
            print("🎉 SUCCESS! Tafra System is ready for production!")
            print("="*50)
            print("📝 Default Admin Credentials:")
            print("   Username: admin")
            print("   Password: admin123")
            print("   ⚠️  IMPORTANT: Change the password after first login!")
            print("\n📍 System Information:")
            print(f"   Database: {app.config['SQLALCHEMY_DATABASE_URI']}")
            print(f"   Environment: {os.environ.get('FLASK_CONFIG', 'development')}")
            print(f"   Initialization Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("="*50)
            
        except Exception as e:
            print(f"❌ Error during initialization: {str(e)}")
            print("🔧 Troubleshooting tips:")
            print("   1. Check database file permissions")
            print("   2. Ensure the database directory exists")
            print("   3. Check PythonAnywhere console for detailed errors")
            return False
    
    return True

if __name__ == "__main__":
    print("🔧 PythonAnywhere Database Initialization")
    print("📋 This script will:")
    print("   - Create all database tables")
    print("   - Set up the default admin user")
    print("   - Configure the system for production")
    
    # Ask for confirmation
    response = input("\n🤔 Do you want to continue? (y/N): ").lower().strip()
    
    if response in ['y', 'yes']:
        success = initialize_database()
        if success:
            print("✨ Initialization completed successfully!")
            print("🌐 Your Tafra system is now ready to use!")
        else:
            print("💥 Initialization failed. Please check the errors above.")
            sys.exit(1)
    else:
        print("⏹️ Initialization cancelled.")
        sys.exit(0) 