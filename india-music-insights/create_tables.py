#!/usr/bin/env python3
"""
Script to manually create database tables
"""

import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.db import init_db
from app import models

if __name__ == "__main__":
    print("Creating database tables...")
    try:
        init_db()
        print("✅ Database tables created successfully!")
    except Exception as e:
        print(f"❌ Failed to create tables: {e}")
        sys.exit(1)
