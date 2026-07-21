# check_all_mysql.py - Check all MySQL tables

import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="skillbridge"
    )
    
    cursor = conn.cursor()
    
    tables = ["Users", "Analyses", "Missing_Skills", "Roadmap_Steps", "Resume_Tips"]
    
    print("=" * 60)
    print("📊 SKILLBRIDGE DATABASE SUMMARY")
    print("=" * 60)
    
    total_rows = 0
    
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"  📄 {table}: {count} rows")
        total_rows += count
        
        # Show sample data
        if count > 0:
            cursor.execute(f"SELECT * FROM {table} LIMIT 2")
            rows = cursor.fetchall()
            for row in rows:
                print(f"     {str(row)[:50]}...")
    
    print("=" * 60)
    print(f"📊 Total rows: {total_rows}")
    
    conn.close()
    
except Exception as e:
    print(f"❌ Error: {e}")