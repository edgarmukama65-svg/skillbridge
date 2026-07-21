# migrate_analyses_manual.py - Manual migration of analyses

import sqlite3
import mysql.connector
import json
from datetime import datetime

print("=" * 60)
print("🔄 MANUAL MIGRATION OF ANALYSES")
print("=" * 60)

# Step 1: Get analyses from SQLite
print("\n📂 Reading analyses from SQLite...")
sqlite_conn = sqlite3.connect("skillbridge.db")
sqlite_cursor = sqlite_conn.cursor()

# Get column names first
sqlite_cursor.execute("PRAGMA table_info(Analyses)")
columns_info = sqlite_cursor.fetchall()
column_names = [col[1] for col in columns_info]
print(f"📋 Columns: {column_names}")

# Get all analyses
sqlite_cursor.execute("SELECT * FROM Analyses")
sqlite_analyses = sqlite_cursor.fetchall()
sqlite_conn.close()

if not sqlite_analyses:
    print("⚠️ No analyses found in SQLite")
    exit()

print(f"📋 Found {len(sqlite_analyses)} analyses in SQLite")

# Step 2: Connect to MySQL
print("\n📂 Connecting to MySQL...")
try:
    mysql_conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="skillbridge"
    )
    mysql_cursor = mysql_conn.cursor()
    print("✅ MySQL connected successfully!")
except Exception as e:
    print(f"❌ MySQL connection failed: {e}")
    exit()

# Step 3: Migrate each analysis
print("\n🔄 Migrating analyses to MySQL...")

migrated_count = 0
skipped_count = 0

for analysis in sqlite_analyses:
    try:
        print(f"📄 Analysis data: {analysis}")
        
        # Map based on position
        analysis_id = analysis[0] if len(analysis) > 0 else None
        user_id = analysis[1] if len(analysis) > 1 else None
        resume_text = analysis[2] if len(analysis) > 2 and analysis[2] else ""
        job_title = analysis[3] if len(analysis) > 3 and analysis[3] else "Software Engineer"
        job_desc = analysis[4] if len(analysis) > 4 and analysis[4] else ""
        ats_score = analysis[5] if len(analysis) > 5 and analysis[5] else 0
        skills_have = analysis[6] if len(analysis) > 6 and analysis[6] else "[]"
        skills_need = analysis[7] if len(analysis) > 7 and analysis[7] else "[]"
        created_at = analysis[8] if len(analysis) > 8 and analysis[8] else datetime.now().isoformat()
        
        print(f"  📄 ID: {analysis_id}, User: {user_id}, Job: {job_title}, Score: {ats_score}")
        
        if not analysis_id or not user_id:
            print(f"  ⚠️ Missing ID or UserId, skipping")
            skipped_count += 1
            continue
        
        # Check if analysis already exists in MySQL
        mysql_cursor.execute("SELECT Id FROM Analyses WHERE Id = %s", (analysis_id,))
        if mysql_cursor.fetchone():
            print(f"  ⏭️ Skipping {analysis_id} (already exists)")
            skipped_count += 1
            continue
        
        # Insert into MySQL
        mysql_cursor.execute("""
            INSERT INTO Analyses (
                Id, UserId, ResumeText, JobTitle, JobDescription, AtsScore,
                SkillsHave, SkillsNeed, CreatedAt
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            analysis_id, user_id, resume_text[:500], job_title,
            job_desc[:500], ats_score, skills_have, skills_need, created_at
        ))
        
        print(f"  ✅ Migrated: {analysis_id}")
        migrated_count += 1
        
    except mysql.connector.Error as e:
        print(f"  ❌ MySQL Error: {e}")
        skipped_count += 1
    except Exception as e:
        print(f"  ❌ Error: {e}")
        skipped_count += 1

# Commit and close
mysql_conn.commit()
mysql_conn.close()

# Show results
print("\n" + "=" * 60)
print("✅ MIGRATION COMPLETE!")
print("=" * 60)
print(f"📊 Analyses migrated: {migrated_count}")
print(f"📊 Analyses skipped: {skipped_count}")

# Verify in MySQL
print("\n📋 Analyses now in MySQL:")
try:
    mysql_conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="skillbridge"
    )
    mysql_cursor = mysql_conn.cursor()
    mysql_cursor.execute("SELECT Id, JobTitle, AtsScore, CreatedAt FROM Analyses")
    mysql_analyses = mysql_cursor.fetchall()
    if mysql_analyses:
        for a in mysql_analyses:
            print(f"  📄 {a[0]} | {a[1]} | Score: {a[2]}% | {a[3][:16] if a[3] else 'No Date'}")
    else:
        print("  ❌ No analyses found in MySQL")
    mysql_conn.close()
except Exception as e:
    print(f"❌ Error verifying: {e}")