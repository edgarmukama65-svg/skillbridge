# check_sqlite.py - Check SQLite database structure

import sqlite3

conn = sqlite3.connect('skillbridge.db')
cursor = conn.cursor()

# Check tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("📋 Tables in SQLite:")
for table in tables:
    print(f"  - {table[0]}")

# Check Analyses table structure
cursor.execute("PRAGMA table_info(Analyses)")
columns = cursor.fetchall()
print("\n📋 Analyses table columns:")
for col in columns:
    print(f"  {col[1]} ({col[2]})")

# Check data in Analyses
cursor.execute("SELECT * FROM Analyses")
analyses = cursor.fetchall()
print(f"\n📊 Analyses data ({len(analyses)} rows):")
for row in analyses:
    print(f"  {row}")

conn.close()