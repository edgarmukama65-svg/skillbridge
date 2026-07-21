# migrate_all_final.py - Complete migration script

import sqlite3
import mysql.connector
from datetime import datetime

print("=" * 60)
print("🔄 COMPLETE MIGRATION TO MYSQL")
print("=" * 60)

# ============================================
# CONNECT TO SQLITE
# ============================================
print("\n📂 Reading from SQLite...")
sqlite_conn = sqlite3.connect('skillbridge.db')
sqlite_cursor = sqlite_conn.cursor()

# ============================================
# CONNECT TO MYSQL
# ============================================
print("📂 Connecting to MySQL...")
try:
    mysql_conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="skillbridge"
    )
    mysql_cursor = mysql_conn.cursor()
    print("✅ MySQL connected!")
except Exception as e:
    print(f"❌ MySQL connection failed: {e}")
    exit()

# ============================================
# MIGRATE MISSING_SKILLS
# ============================================
print("\n📋 Migrating Missing_Skills...")
sqlite_cursor.execute("SELECT * FROM Missing_Skills")
data = sqlite_cursor.fetchall()
print(f"  Found {len(data)} rows")

migrated = 0
for row in data:
    try:
        mysql_cursor.execute("""
            INSERT IGNORE INTO Missing_Skills 
            (Id, AnalysisId, SkillName, Importance, Reason, CreatedAt)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, row)
        migrated += 1
    except Exception as e:
        print(f"  ❌ Error: {e}")
print(f"  ✅ Migrated {migrated} rows")

# ============================================
# MIGRATE ROADMAP_STEPS
# ============================================
print("\n📋 Migrating Roadmap_Steps...")
sqlite_cursor.execute("SELECT * FROM Roadmap_Steps")
data = sqlite_cursor.fetchall()
print(f"  Found {len(data)} rows")

migrated = 0
for row in data:
    try:
        mysql_cursor.execute("""
            INSERT IGNORE INTO Roadmap_Steps 
            (Id, AnalysisId, StepOrder, ActionItem, ResourceUrl, ResourceType, 
             EstimatedTime, Priority, IsCompleted, CreatedAt)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, row)
        migrated += 1
    except Exception as e:
        print(f"  ❌ Error: {e}")
print(f"  ✅ Migrated {migrated} rows")

# ============================================
# MIGRATE RESUME_TIPS
# ============================================
print("\n📋 Migrating Resume_Tips...")
sqlite_cursor.execute("SELECT * FROM Resume_Tips")
data = sqlite_cursor.fetchall()
print(f"  Found {len(data)} rows")

migrated = 0
for row in data:
    try:
        mysql_cursor.execute("""
            INSERT IGNORE INTO Resume_Tips 
            (Id, AnalysisId, TipOrder, TipText, Category, Priority, CreatedAt)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, row)
        migrated += 1
    except Exception as e:
        print(f"  ❌ Error: {e}")
print(f"  ✅ Migrated {migrated} rows")

# ============================================
# COMMIT AND CLOSE
# ============================================
mysql_conn.commit()
mysql_conn.close()
sqlite_conn.close()

# ============================================
# VERIFY
# ============================================
print("\n📋 Verifying in MySQL...")
try:
    mysql_conn = mysql.connector.connect(
        host="localhost", user="root", password="", database="skillbridge"
    )
    mysql_cursor = mysql_conn.cursor()
    
    tables = ['Missing_Skills', 'Roadmap_Steps', 'Resume_Tips']
    for table in tables:
        mysql_cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = mysql_cursor.fetchone()[0]
        print(f"  📄 {table}: {count} rows")
    
    mysql_conn.close()
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 60)
print("✅ MIGRATION COMPLETE!")
print("=" * 60)