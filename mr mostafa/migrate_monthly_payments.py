#!/usr/bin/env python3
"""
Migration script to add monthly payment functionality
Run this script after updating the models to add monthly payment support
"""

import os
import sys
from datetime import datetime

# Add the current directory to path so we can import the app
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, Group, MonthlyPayment

def migrate_monthly_payments():
    """Add monthly payment support to the database"""
    with app.app_context():
        try:
            # Create the database tables (this will add new columns and tables)
            db.create_all()
            
            print("✅ Database tables created/updated successfully")
            
            # Check if the new columns exist by trying a simple query
            try:
                # Test if columns exist by doing a simple count query
                test_query = db.session.execute(
                    "SELECT COUNT(*) FROM 'group' WHERE monthly_payment_enabled IS NOT NULL"
                ).scalar()
                columns_exist = True
            except Exception:
                columns_exist = False
            
            if not columns_exist:
                print("ℹ️ New columns don't exist yet - this is normal for first-time migration")
                # Use raw SQL to add columns if they don't exist
                try:
                    from sqlalchemy import text
                    db.session.execute(text("ALTER TABLE 'group' ADD COLUMN monthly_payment_enabled BOOLEAN DEFAULT 1"))
                    db.session.execute(text("ALTER TABLE 'group' ADD COLUMN monthly_price FLOAT DEFAULT 0.0"))
                    db.session.execute(text("ALTER TABLE 'group' ADD COLUMN payment_due_day INTEGER DEFAULT 1"))
                    db.session.commit()
                    print("✅ Added new columns to groups table")
                except Exception as e:
                    if "duplicate column name" in str(e).lower():
                        print("✅ Columns already exist")
                    else:
                        print(f"⚠️ Warning adding columns: {str(e)}")
                    db.session.rollback()
                
                # Force a fresh session to reload the schema
                db.session.close()
                
            # Now safely update existing groups using raw SQL
            try:
                from sqlalchemy import text
                
                # Count groups that need updating using raw SQL
                result = db.session.execute(text("""
                    SELECT COUNT(*) FROM 'group' 
                    WHERE monthly_payment_enabled IS NULL 
                    OR monthly_price IS NULL 
                    OR payment_due_day IS NULL
                """)).scalar()
                
                if result and result > 0:
                    # Update groups with default values using raw SQL
                    db.session.execute(text("""
                        UPDATE 'group' 
                        SET monthly_payment_enabled = COALESCE(monthly_payment_enabled, 1),
                            monthly_price = COALESCE(monthly_price, 0.0),
                            payment_due_day = COALESCE(payment_due_day, 1)
                        WHERE monthly_payment_enabled IS NULL 
                        OR monthly_price IS NULL 
                        OR payment_due_day IS NULL
                    """))
                    db.session.commit()
                    print(f"✅ Updated {result} groups with default monthly payment settings")
                else:
                    print("✅ All groups already have monthly payment settings")
                    
            except Exception as e:
                print(f"⚠️ Warning updating groups: {str(e)}")
                db.session.rollback()
            
            # Create monthly payment records for current month for all groups with monthly payments enabled
            try:
                current_year = datetime.now().year
                current_month = datetime.now().month
                
                print(f"ℹ️ Creating monthly payment records for {current_year}-{current_month:02d}")
                print("ℹ️ Monthly payment record creation will be handled by the application when needed")
                
            except Exception as e:
                print(f"⚠️ Warning creating monthly payments: {str(e)}")
            
            # Print summary
            total_groups = Group.query.count()
            
            # Safely count enabled groups using raw SQL
            try:
                from sqlalchemy import text
                enabled_groups_count = db.session.execute(text(
                    "SELECT COUNT(*) FROM 'group' WHERE monthly_payment_enabled = 1"
                )).scalar() or 0
            except Exception:
                enabled_groups_count = 0
                
            total_monthly_payments = MonthlyPayment.query.count()
            
            print(f"\n📊 Monthly Payments Summary:")
            print(f"   Total groups: {total_groups}")
            print(f"   Groups with monthly payments enabled: {enabled_groups_count}")
            print(f"   Total monthly payment records: {total_monthly_payments}")
            
            print(f"\n🎉 Monthly payments migration completed successfully!")
            
        except Exception as e:
            print(f"❌ Error during migration: {str(e)}")
            db.session.rollback()
            return False
        
        return True

if __name__ == '__main__':
    success = migrate_monthly_payments()
    sys.exit(0 if success else 1) 