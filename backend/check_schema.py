#!/usr/bin/env python3
"""
Check database schema
"""
import sys
import os
sys.path.append('.')
sys.path.append('./app')

from app.core.database import engine
from sqlalchemy import text, inspect

def check_table_schema():
    print("🔍 Checking database schema...")
    
    # Check what tables exist
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f"📋 Available tables: {tables}")
    
    # Check users table structure
    if 'users' in tables:
        print("\n👤 Users table columns:")
        columns = inspector.get_columns('users')
        for col in columns:
            print(f"  - {col['name']}: {col['type']}")
    
    # Check all tables structure
    for table_name in tables:
        print(f"\n📊 {table_name.upper()} table columns:")
        columns = inspector.get_columns(table_name)
        for col in columns:
            print(f"  - {col['name']}: {col['type']}")

if __name__ == "__main__":
    check_table_schema()
