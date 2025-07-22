#!/usr/bin/env python3
"""
Database migration script to add permission fields to User table
This script adds granular permission fields for role-based access control
"""

import os
import sys
import sqlite3
from datetime import datetime

# Add the project directory to the Python path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

from app import app, db, User
from config import config

def migrate_permissions():
    """Add permission fields to User table and set default permissions"""
    
    print("🚀 Starting permissions migration...")
    print("=" * 50)
    
    with app.app_context():
        try:
            # Get database connection for raw SQL operations
            db_uri = app.config['SQLALCHEMY_DATABASE_URI']
            if 'sqlite' in db_uri:
                db_path = db_uri.replace('sqlite:///', '')
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
            else:
                print("❌ This migration script is designed for SQLite databases only")
                return False

            # List of permission fields to add
            permission_fields = [
                'can_manage_payments',
                'can_take_attendance', 
                'can_view_reports',
                'can_manage_students',
                'can_manage_groups',
                'can_manage_instructors',
                'can_manage_users',
                'can_manage_subjects',
                'can_export_data',
                'can_import_data',
                'can_manage_expenses',
                'can_manage_tasks'
            ]

            print("📊 Adding permission columns to User table...")
            
            # Add each permission field to the User table
            for field in permission_fields:
                try:
                    cursor.execute(f'ALTER TABLE user ADD COLUMN {field} BOOLEAN DEFAULT FALSE')
                    print(f"  ✅ Added column: {field}")
                except sqlite3.OperationalError as e:
                    if "duplicate column name" in str(e).lower():
                        print(f"  ⚠️  Column {field} already exists, skipping...")
                    else:
                        print(f"  ❌ Error adding column {field}: {e}")
                        raise

            # Commit the schema changes
            conn.commit()
            print("✅ Permission columns added successfully!")

            # Close the raw connection and force SQLAlchemy to reload schema
            conn.close()
            db.session.close()

            print("\n👥 Setting default permissions for existing users...")

            # Query existing users
            users = User.query.all()
            
            for user in users:
                print(f"  👤 Processing user: {user.username} (Role: {user.role})")
                
                if user.role == 'admin':
                    # Admin users get all permissions automatically via has_permission method
                    # But we'll also set the flags for consistency
                    user.can_manage_payments = True
                    user.can_take_attendance = True
                    user.can_view_reports = True
                    user.can_manage_students = True
                    user.can_manage_groups = True
                    user.can_manage_instructors = True
                    user.can_manage_users = True
                    user.can_manage_subjects = True
                    user.can_export_data = True
                    user.can_import_data = True
                    user.can_manage_expenses = True
                    user.can_manage_tasks = True
                    print(f"    ✅ Set admin permissions for {user.username}")
                
                elif user.role == 'instructor':
                    # Set default instructor permissions (full instructor)
                    user.can_take_attendance = True
                    user.can_view_reports = True
                    user.can_manage_students = True
                    user.can_manage_groups = True
                    user.can_manage_subjects = True
                    user.can_manage_tasks = True
                    print(f"    ✅ Set instructor permissions for {user.username}")
                
                else:
                    # Other roles start with no permissions
                    print(f"    ⚠️  User {user.username} has role '{user.role}' - no default permissions set")

            # Commit all user permission updates
            db.session.commit()
            print("✅ User permissions updated successfully!")

            print("\n📋 Migration Summary:")
            print("-" * 30)
            
            # Display summary of users and their permissions
            users = User.query.all()
            for user in users:
                permissions = user.get_permissions_list()
                print(f"👤 {user.username} ({user.role}): {len(permissions)} permissions")
                if permissions:
                    print(f"   📝 {', '.join(permissions[:3])}{'...' if len(permissions) > 3 else ''}")
                else:
                    print(f"   📝 No permissions")

            print("\n" + "=" * 50)
            print("🎉 SUCCESS! Permission system migration completed!")
            print("=" * 50)
            print("📝 Next Steps:")
            print("   1. Test user login and access control")
            print("   2. Assign specific permissions to users as needed")
            print("   3. Update route decorators to use new permission system")
            print(f"   4. Migration completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("=" * 50)

            return True

        except Exception as e:
            print(f"❌ Error during migration: {str(e)}")
            print("🔧 Rolling back changes...")
            db.session.rollback()
            print("🔧 Troubleshooting tips:")
            print("   1. Ensure the database file exists and is writable")
            print("   2. Check that no other processes are using the database")
            print("   3. Verify SQLite database integrity")
            print("   4. Check application logs for detailed errors")
            return False

if __name__ == '__main__':
    print("🔧 Permission System Migration Tool")
    print("=" * 50)
    
    # Load configuration
    config_name = os.environ.get('FLASK_CONFIG', 'development')
    app.config.from_object(config[config_name])
    
    print(f"📍 Environment: {config_name}")
    print(f"📍 Database: {app.config['SQLALCHEMY_DATABASE_URI']}")
    
    # Confirm before running
    response = input("\n❓ Do you want to run the permission migration? (y/N): ")
    if response.lower() in ['y', 'yes']:
        success = migrate_permissions()
        sys.exit(0 if success else 1)
    else:
        print("❌ Migration cancelled by user")
        sys.exit(1) 