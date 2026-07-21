# migrate_all_data.py - Migrate all data from SQLite to MySQL

import sqlite3
import mysql.connector
import json
from datetime import datetime

print("=" * 70)
print("🔄 MIGRATING ALL DATA FROM SQLITE TO MYSQL")
print("=" * 70)

# ============================================
# SQLITE CONNECTION
# ============================================

def get_sqlite_data(table_name):
    """Get all data from a SQLite table"""
    try:
        conn = sqlite3.connect('skillbridge.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        data = cursor.fetchall()
        conn.close()
        return data
    except Exception as e:
        print(f"❌ Error reading {table_name}: {e}")
        return []

# ============================================
# MYSQL CONNECTION
# ============================================

def get_mysql_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="skillbridge"
        )
        return conn
    except mysql.connector.Error as e:
        print(f"❌ MySQL error: {e}")
        return None

# ============================================
# MIGRATION FUNCTIONS
# ============================================

def migrate_table(table_name, columns, data, id_column='Id'):
    """Migrate data to a specific table"""
    if not data:
        print(f"⚠️ No data in {table_name}")
        return 0
    
    mysql_conn = get_mysql_connection()
    if mysql_conn is None:
        return 0
    
    mysql_cursor = mysql_conn.cursor()
    
    # Build the insert query
    placeholders = ', '.join(['%s'] * len(columns))
    column_names = ', '.join(columns)
    query = f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})"
    
    migrated = 0
    skipped = 0
    
    for row in data:
        try:
            # Check if record already exists
            if id_column and row[0]:
                mysql_cursor.execute(f"SELECT {id_column} FROM {table_name} WHERE {id_column} = %s", (row[0],))
                if mysql_cursor.fetchone():
                    print(f"  ⏭️ {table_name} {row[0]} already exists")
                    skipped += 1
                    continue
            
            mysql_cursor.execute(query, row)
            migrated += 1
            print(f"  ✅ {table_name} row migrated")
            
        except mysql.connector.Error as e:
            print(f"  ❌ Error migrating {table_name}: {e}")
            skipped += 1
        except Exception as e:
            print(f"  ❌ Error: {e}")
            skipped += 1
    
    mysql_conn.commit()
    mysql_conn.close()
    
    return migrated, skipped

# ============================================
# MAIN MIGRATION
# ============================================

# Step 1: Check what's in SQLite
print("\n📂 Checking SQLite data...")
sqlite_conn = sqlite3.connect('skillbridge.db')
sqlite_cursor = sqlite_conn.cursor()
sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = sqlite_cursor.fetchall()
sqlite_conn.close()

print("📋 Tables found in SQLite:")
for table in tables:
    print(f"  - {table[0]}")

# Step 2: Migrate each table
print("\n🔄 Starting migration...")

# Table definitions: (table_name, columns, id_column)
table_definitions = [
    ("Missing_Skills", ['Id', 'AnalysisId', 'SkillName', 'Importance', 'Reason', 'CreatedAt'], 'Id'),
    ("Roadmap_Steps", ['Id', 'AnalysisId', 'StepOrder', 'ActionItem', 'ResourceUrl', 'ResourceType', 'EstimatedTime', 'Priority', 'IsCompleted', 'CreatedAt'], 'Id'),
    ("Resume_Tips", ['Id', 'AnalysisId', 'TipOrder', 'TipText', 'Category', 'Priority', 'CreatedAt'], 'Id'),
]

total_migrated = 0
total_skipped = 0

for table_name, columns, id_column in table_definitions:
    print(f"\n📋 Migrating {table_name}...")
    data = get_sqlite_data(table_name)
    if data:
        print(f"  Found {len(data)} rows in SQLite")
        migrated, skipped = migrate_table(table_name, columns, data, id_column)
        total_migrated += migrated
        total_skipped += skipped
        print(f"  ✅ {table_name}: {migrated} migrated, {skipped} skipped")
    else:
        print(f"  ⚠️ No data in {table_name}")

# Step 3: Show results
print("\n" + "=" * 70)
print("✅ MIGRATION COMPLETE!")
print("=" * 70)
print(f"📊 Total migrated: {total_migrated}")
print(f"📊 Total skipped: {total_skipped}")

# Step 4: Verify in MySQL
print("\n📋 Verifying data in MySQL:")
mysql_conn = get_mysql_connection()
if mysql_conn:
    mysql_cursor = mysql_conn.cursor()
    
    for table_name, _, _ in table_definitions:
        mysql_cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = mysql_cursor.fetchone()[0]
        print(f"  📄 {table_name}: {count} rows")
    
    mysql_conn.close()