#!/usr/bin/env python3
"""
Migration script to add grades functionality
Run this script after updating the models to add grades support
"""

import os
import sys
from datetime import datetime

# Add the current directory to path so we can import the app
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, Subject, Grade, Student, Group

def migrate_grades():
    """Add grades support to the database"""
    with app.app_context():
        try:
            # Create the database tables (this will add new tables)
            db.create_all()
            
            print("✅ Database tables created successfully")
            
            # Create some default subjects if none exist
            if Subject.query.count() == 0:
                default_subjects = [
                    {
                        'name': 'الرياضيات',
                        'subject_type': 'مادة',
                        'max_grade': 100.0,
                        'description': 'مادة الرياضيات الأساسية'
                    },
                    {
                        'name': 'العلوم',
                        'subject_type': 'مادة', 
                        'max_grade': 100.0,
                        'description': 'مادة العلوم العامة'
                    },
                    {
                        'name': 'اللغة العربية',
                        'subject_type': 'مادة',
                        'max_grade': 100.0,
                        'description': 'مادة اللغة العربية'
                    },
                    {
                        'name': 'اللغة الإنجليزية', 
                        'subject_type': 'مادة',
                        'max_grade': 100.0,
                        'description': 'مادة اللغة الإنجليزية'
                    }
                ]
                
                subjects_created = 0
                for subject_data in default_subjects:
                    subject = Subject(**subject_data)
                    db.session.add(subject)
                    subjects_created += 1
                
                db.session.commit()
                print(f"✅ Created {subjects_created} default subjects")
            else:
                print("✅ Subjects already exist")
            
            # Try to link some subjects to existing groups using new many-to-many relationship
            subjects = Subject.query.all()
            groups = Group.query.all()
            
            if subjects and groups:
                linked_count = 0
                for subject in subjects:
                    if not subject.groups:
                        # Try to find a matching group based on subject name
                        for group in groups:
                            if any(keyword in group.name.lower() for keyword in subject.name.lower().split()):
                                group.subjects.append(subject)
                                linked_count += 1
                                break
                
                if linked_count > 0:
                    db.session.commit()
                    print(f"✅ Linked {linked_count} subjects to groups")
            
            # Print summary
            total_subjects = Subject.query.count()
            total_grades = Grade.query.count()
            total_students = Student.query.count()
            
            print(f"\n📊 Grades System Summary:")
            print(f"   Total subjects: {total_subjects}")
            print(f"   Total grades recorded: {total_grades}")
            print(f"   Total students: {total_students}")
            print(f"   Active subjects: {Subject.query.filter_by(is_active=True).count()}")
            
            # Show some examples
            if total_subjects > 0:
                print(f"\n📚 Available Subjects:")
                for subject in Subject.query.limit(5).all():
                    group_info = f" (المجموعة: {subject.group.name})" if subject.group else ""
                    print(f"   • {subject.name} - {subject.subject_type}{group_info}")
            
            print(f"\n🎉 Grades system migration completed successfully!")
            print(f"🔗 Access the grades system at: /grades")
            print(f"📤 Download grades template at: /download_grades_template")
            print(f"📥 Import grades at: /import_grades")
            
        except Exception as e:
            print(f"❌ Error during migration: {str(e)}")
            db.session.rollback()
            return False
        
        return True

if __name__ == '__main__':
    success = migrate_grades()
    sys.exit(0 if success else 1) 