#!/usr/bin/env python3
"""
Migration script to add grade_level field to students
Run this script after updating the Student model to add grade level support
"""

import os
import sys
from datetime import datetime

# Add the current directory to path so we can import the app
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, Student

def migrate_grade_levels():
    """Add grade_level field to students"""
    with app.app_context():
        try:
            # Create the database tables (this will add new columns)
            db.create_all()
            
            print("✅ Database tables updated successfully")
            
            # Check if the grade_level column exists
            try:
                from sqlalchemy import text
                test_query = db.session.execute(
                    text("SELECT COUNT(*) FROM student WHERE grade_level IS NOT NULL")
                ).scalar()
                columns_exist = True
            except Exception:
                columns_exist = False
            
            if not columns_exist:
                print("ℹ️ Grade level column doesn't exist yet - adding it")
                try:
                    db.session.execute(text("ALTER TABLE student ADD COLUMN grade_level VARCHAR(50)"))
                    db.session.commit()
                    print("✅ Added grade_level column to students table")
                except Exception as e:
                    if "duplicate column name" in str(e).lower():
                        print("✅ Grade level column already exists")
                    else:
                        print(f"⚠️ Warning adding column: {str(e)}")
                    db.session.rollback()
                
                # Force a fresh session to reload the schema
                db.session.close()
            
            # Check if any students need default grade levels using raw SQL
            try:
                from sqlalchemy import text
                students_needing_update = db.session.execute(text("""
                    SELECT id, age FROM student 
                    WHERE grade_level IS NULL OR grade_level = ''
                """)).fetchall()
            except Exception as e:
                print(f"⚠️ Warning querying students: {str(e)}")
                students_needing_update = []
            
            # Suggest grade levels based on age if available
            age_to_grade_mapping = {
                4: 'رياض الأطفال - KG1',
                5: 'رياض الأطفال - KG2', 
                6: 'الصف الأول الابتدائي',
                7: 'الصف الثاني الابتدائي',
                8: 'الصف الثالث الابتدائي',
                9: 'الصف الرابع الابتدائي',
                10: 'الصف الخامس الابتدائي',
                11: 'الصف السادس الابتدائي',
                12: 'الصف الأول الإعدادي',
                13: 'الصف الثاني الإعدادي',
                14: 'الصف الثالث الإعدادي',
                15: 'الصف الأول الثانوي',
                16: 'الصف الثاني الثانوي',
                17: 'الصف الثالث الثانوي',
                18: 'جامعي',
                19: 'جامعي',
                20: 'جامعي'
            }
            
            updated_count = 0
            for student_row in students_needing_update:
                student_id = student_row[0]
                student_age = student_row[1]
                
                grade_level = None
                if student_age and student_age in age_to_grade_mapping:
                    grade_level = age_to_grade_mapping[student_age]
                elif student_age and student_age > 20:
                    grade_level = 'جامعي'
                elif student_age and student_age < 4:
                    grade_level = 'رياض الأطفال - KG1'
                
                if grade_level:
                    try:
                        db.session.execute(text(
                            "UPDATE student SET grade_level = :grade_level WHERE id = :student_id"
                        ), {"grade_level": grade_level, "student_id": student_id})
                        updated_count += 1
                    except Exception as e:
                        print(f"⚠️ Warning updating student {student_id}: {str(e)}")
            
            if updated_count > 0:
                db.session.commit()
                print(f"✅ Updated {updated_count} students with suggested grade levels based on age")
            else:
                print("ℹ️ No students needed automatic grade level assignment")
            
            # Print summary using raw SQL
            try:
                from sqlalchemy import text
                total_students = db.session.execute(text("SELECT COUNT(*) FROM student")).scalar() or 0
                students_with_grade_level = db.session.execute(text(
                    "SELECT COUNT(*) FROM student WHERE grade_level IS NOT NULL AND grade_level != ''"
                )).scalar() or 0
                students_without_grade_level = total_students - students_with_grade_level
                
                print(f"\n📊 Grade Levels Summary:")
                print(f"   Total students: {total_students}")
                print(f"   Students with grade level: {students_with_grade_level}")
                print(f"   Students without grade level: {students_without_grade_level}")
                
                # Show grade level distribution
                if students_with_grade_level > 0:
                    print(f"\n📚 Grade Level Distribution:")
                    grade_levels = db.session.execute(text("""
                        SELECT grade_level, COUNT(*) as count 
                        FROM student 
                        WHERE grade_level IS NOT NULL AND grade_level != ''
                        GROUP BY grade_level
                        ORDER BY grade_level
                    """)).fetchall()
                    
                    for row in grade_levels:
                        grade_level, count = row
                        print(f"   • {grade_level}: {count} طالب")
                        
            except Exception as e:
                print(f"⚠️ Warning generating summary: {str(e)}")
            
            print(f"\n🎉 Grade levels migration completed successfully!")
            print(f"💡 Note: Students without grade levels can be updated manually through the interface")
            
        except Exception as e:
            print(f"❌ Error during migration: {str(e)}")
            db.session.rollback()
            return False
        
        return True

if __name__ == '__main__':
    success = migrate_grade_levels()
    sys.exit(0 if success else 1) 