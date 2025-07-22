#!/usr/bin/env python3
"""
Migration script to add completion fields to existing groups
Run this script after updating the Group model to add completion fields
"""

import os
import sys
from datetime import datetime

# Add the current directory to path so we can import the app
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, Group

def migrate_groups_completion():
    """Add completion fields to existing groups"""
    with app.app_context():
        try:
            # Create the database tables (this will add new columns)
            db.create_all()
            
            # Update existing groups that don't have status set
            groups_to_update = Group.query.filter(
                (Group.status == None) | (Group.status == '')
            ).all()
            
            updated_count = 0
            for group in groups_to_update:
                group.status = 'active'  # Set default status to active
                updated_count += 1
            
            if updated_count > 0:
                db.session.commit()
                print(f"✅ Updated {updated_count} groups with default status 'active'")
            else:
                print("✅ All groups already have status set")
                
            # Print summary
            active_groups = Group.query.filter_by(status='active').count()
            completed_groups = Group.query.filter_by(status='completed').count()
            total_groups = Group.query.count()
            
            print(f"\n📊 Groups Summary:")
            print(f"   Total groups: {total_groups}")
            print(f"   Active groups: {active_groups}")
            print(f"   Completed groups: {completed_groups}")
            
            print(f"\n🎉 Migration completed successfully!")
            
        except Exception as e:
            print(f"❌ Error during migration: {str(e)}")
            db.session.rollback()
            return False
    
    return True

if __name__ == '__main__':
    print("🚀 Starting Group Completion Migration...")
    print("="*50)
    
    success = migrate_groups_completion()
    
    if success:
        print("\n✅ Migration completed successfully!")
        print("You can now use the group completion features.")
    else:
        print("\n❌ Migration failed!")
        sys.exit(1) 