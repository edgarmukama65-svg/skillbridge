# test_mysql.py - Test MySQL Connection

from database import get_connection, get_all_users

print("🔄 Testing MySQL connection...")

conn = get_connection()
if conn:
    print("✅ MySQL connected successfully!")
    conn.close()
else:
    print("❌ MySQL connection failed!")
    print("   Make sure XAMPP MySQL is running")

print("\n📋 Users in database:")
users = get_all_users()
if users:
    for user in users:
        print(f"  👤 {user[1]} ({user[2]}) - Role: {user[3]}")
else:
    print("  No users found")