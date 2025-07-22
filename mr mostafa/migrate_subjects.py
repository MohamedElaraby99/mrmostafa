#!/usr/bin/env python3
"""
Migration script to migrate from level system to subjects system
Run this script after updating the models to use subjects instead of levels
"""

import os
import sys
from datetime import datetime

# Add the current directory to path so we can import the app
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, Group, Subject

def migrate_subjects():
    """Migrate from level system to subjects system"""
    with app.app_context():
        try:
            print("🔄 بدء ترحيل النظام من المستويات إلى المواد...")
            
            # Create the database tables (this will add new tables and relationships)
            db.create_all()
            print("✅ تم إنشاء جداول قاعدة البيانات")
            
            # Check if level column exists in database using raw SQL
            from sqlalchemy import text
            try:
                # Check if level column exists
                result = db.session.execute(text("PRAGMA table_info(group)"))
                columns = [row[1] for row in result.fetchall()]
                has_level_column = 'level' in columns
                
                if not has_level_column:
                    print("ℹ️ عمود المستوى غير موجود في قاعدة البيانات - لا حاجة للترحيل")
                    return
                
                # Get all groups that have levels using raw SQL
                result = db.session.execute(text("SELECT id, name, level FROM group WHERE level IS NOT NULL AND level != ''"))
                groups_data = result.fetchall()
                
                if not groups_data:
                    print("ℹ️ لا توجد مجموعات بمستويات لترحيلها")
                    return
                
                print(f"📊 وجد {len(groups_data)} مجموعة بمستويات")
                
                # Create subjects from unique levels
                unique_levels = set()
                groups_info = {}  # Store group id -> (name, level) mapping
                
                for group_row in groups_data:
                    group_id, group_name, level = group_row
                    if level and level.strip():
                        unique_levels.add(level.strip())
                        groups_info[group_id] = (group_name, level.strip())
            
            print(f"🔍 وجد {len(unique_levels)} مستوى فريد: {', '.join(unique_levels)}")
            
            # Create subjects for each unique level
            created_subjects = {}
            for level in unique_levels:
                existing_subject = Subject.query.filter_by(name=level).first()
                if existing_subject:
                    created_subjects[level] = existing_subject
                    print(f"✅ المادة '{level}' موجودة بالفعل")
                else:
                    # Determine subject type and max grade based on level name
                    subject_type = 'مادة'
                    max_grade = 100.0
                    description = f"مادة مُحوّلة من المستوى: {level}"
                    
                    # Set specific properties based on level name
                    level_lower = level.lower()
                    if 'math' in level_lower or 'رياضيات' in level_lower:
                        subject_type = 'مادة'
                        max_grade = 100.0
                        description = f"مادة الرياضيات - مستوى {level}"
                    elif 'communication' in level_lower or 'تخاطب' in level_lower:
                        subject_type = 'نشاط'
                        max_grade = 100.0
                        description = f"جلسات تخاطب - مستوى {level}"
                    elif 'برمجة' in level_lower or 'سكراتش' in level_lower:
                        subject_type = 'مادة'
                        max_grade = 100.0
                        description = f"مادة البرمجة - مستوى {level}"
                    elif level_lower.startswith('a') and len(level_lower) == 2:  # A1, A2, A3
                        subject_type = 'مادة'
                        max_grade = 100.0
                        description = f"مادة اللغة الإنجليزية - مستوى {level}"
                    
                    subject = Subject(
                        name=level,
                        code=level.upper().replace(' ', '_'),
                        description=description,
                        subject_type=subject_type,
                        max_grade=max_grade,
                        min_grade=0.0,
                        is_active=True
                    )
                    
                    db.session.add(subject)
                    db.session.flush()  # Get the ID
                    created_subjects[level] = subject
                    print(f"✅ تم إنشاء المادة '{level}' (نوع: {subject_type})")
            
                # Link groups to their corresponding subjects
                linked_count = 0
                for group_id, (group_name, level) in groups_info.items():
                    if level in created_subjects:
                        subject = created_subjects[level]
                        group = Group.query.get(group_id)
                        
                        if group and subject not in group.subjects:
                            group.subjects.append(subject)
                            linked_count += 1
                            print(f"🔗 ربط المجموعة '{group_name}' بالمادة '{subject.name}'")
            
            # Commit all changes
            db.session.commit()
            
            print(f"\n🎉 تم الترحيل بنجاح!")
                print(f"📊 الإحصائيات:")
                print(f"   • تم إنشاء {len(created_subjects)} مادة")
                print(f"   • تم ربط {linked_count} مجموعة بمواد")
                print(f"   • إجمالي المجموعات المُحدّثة: {len(groups_info)}")
                
                # Show summary of created subjects
                print(f"\n📚 المواد المُنشأة:")
                for level, subject in created_subjects.items():
                    groups_count = subject.groups.count() if hasattr(subject.groups, 'count') else len(list(subject.groups))
                    print(f"   • {subject.name} ({subject.subject_type}) - مرتبطة بـ {groups_count} مجموعة")
                
                print(f"\n💡 ملاحظة: يمكنك الآن إدارة المواد من صفحة 'إدارة المواد' وربط مواد إضافية بالمجموعات")
                
            except Exception as db_error:
                print(f"❌ خطأ في قاعدة البيانات: {str(db_error)}")
                db.session.rollback()
                raise db_error
            
        except Exception as e:
            print(f"❌ خطأ أثناء الترحيل: {str(e)}")
            db.session.rollback()
            raise e

if __name__ == '__main__':
    migrate_subjects() 