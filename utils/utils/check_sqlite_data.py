# check_sqlite_data.py - Check SQLite tables

import sqlite3

conn = sqlite3.connect('skillbridge.db')
cursor = conn.cursor()

# Check all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()

print("📋 Tables in SQLite:")
for table in tables:
    table_name = table[0]
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    count = cursor.fetchone()[0]
    print(f"  {table_name}: {count} rows")

# Check each table's data
print("\n📊 Table Data:")

# Check Missing_Skills
cursor.execute("SELECT * FROM Missing_Skills")
data = cursor.fetchall()
print(f"\nMissing_Skills: {len(data)} rows")
for row in data:
    print(f"  {row}")

# Check Roadmap_Steps
cursor.execute("SELECT * FROM Roadmap_Steps")
data = cursor.fetchall()
print(f"\nRoadmap_Steps: {len(data)} rows")
for row in data:
    print(f"  {row}")

# Check Resume_Tips
cursor.execute("SELECT * FROM Resume_Tips")
data = cursor.fetchall()
print(f"\nResume_Tips: {len(data)} rows")
for row in data:
    print(f"  {row}")

conn.close()