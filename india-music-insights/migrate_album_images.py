#!/usr/bin/env python3
"""
Database migration to add album image fields to tracks table
"""

import sqlite3
import os
import sys
from pathlib import Path

# Add the app directory to Python path
app_dir = Path(__file__).parent / "app"
sys.path.insert(0, str(app_dir))

def migrate_database():
    """Add album image columns to tracks table"""
    db_path = "india_music_insights.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Database file {db_path} not found")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(tracks)")
        columns = [column[1] for column in cursor.fetchall()]
        
        columns_to_add = [
            ("album_image_url", "VARCHAR(500)"),
            ("album_image_width", "INTEGER"), 
            ("album_image_height", "INTEGER")
        ]
        
        for column_name, column_type in columns_to_add:
            if column_name not in columns:
                print(f"➕ Adding column: {column_name}")
                cursor.execute(f"ALTER TABLE tracks ADD COLUMN {column_name} {column_type}")
            else:
                print(f"✅ Column {column_name} already exists")
        
        conn.commit()
        conn.close()
        
        print("✅ Database migration completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False

if __name__ == "__main__":
    print("🔄 Running database migration for album images...")
    success = migrate_database()
    if success:
        print("🎵 Ready to fetch album artwork from Spotify!")
    else:
        print("💥 Migration failed - check the error above")
    
    sys.exit(0 if success else 1)
