# check_db.py - Check MySQL database directly

import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="skillbridge"
    )
    
    cursor = conn.cursor()
    
    # Show all tables
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    print("📋 Tables in database:")
    for table in tables:
        print(f"  - {table[0]}")
    
    # Show users
    cursor.execute("SELECT Id, Name, Email, Role FROM Users")
    users = cursor.fetchall()
    print("\n📋 Users in database:")
    if users:
        for user in users:
            print(f"  👤 {user[0]} | {user[1]} | {user[2]} | Role: {user[3]}")
    else:
        print("  No users found")
    
    conn.close()
    
except Exception as e:
    print(f"❌ Error: {e}")