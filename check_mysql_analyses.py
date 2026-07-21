# check_mysql_analyses.py - Check analyses in MySQL

import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="skillbridge"
    )
    
    cursor = conn.cursor()
    
    # Check Analyses table
    cursor.execute("SELECT COUNT(*) FROM Analyses")
    count = cursor.fetchone()[0]
    print(f"📊 Total analyses in MySQL: {count}")
    
    if count > 0:
        cursor.execute("SELECT Id, JobTitle, AtsScore, CreatedAt FROM Analyses")
        analyses = cursor.fetchall()
        print("\n📋 Analyses in MySQL:")
        for a in analyses:
            print(f"  📄 {a[0]} | {a[1]} | Score: {a[2]}% | {a[3][:16]}")
    else:
        print("⚠️ No analyses found in MySQL")
    
    conn.close()
    
except Exception as e:
    print(f"❌ Error: {e}")