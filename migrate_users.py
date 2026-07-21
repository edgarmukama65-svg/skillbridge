# migrate_users.py - Migrate users from SQLite to MySQL

import sqlite3
import mysql.connector
from datetime import datetime

# ============================================
# SQLITE CONNECTION
# ============================================

def get_sqlite_connection():
    """Connect to SQLite database"""
    try:
        conn = sqlite3.connect("skillbridge.db")
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        print(f"❌ SQLite error: {e}")
        return None

# ============================================
# MYSQL CONNECTION
# ============================================

def get_mysql_connection():
    """Connect to MySQL database"""
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
# MIGRATE USERS
# ============================================

def migrate_users():
    """Migrate all users from SQLite to MySQL"""
    
    print("=" * 60)
    print("🔄 MIGRATING USERS FROM SQLITE TO MYSQL")
    print("=" * 60)
    
    # Step 1: Get users from SQLite
    print("\n📂 Reading users from SQLite...")
    sqlite_conn = get_sqlite_connection()
    if sqlite_conn is None:
        print("❌ Could not connect to SQLite")
        return
    
    sqlite_cursor = sqlite_conn.cursor()
    
    # Check if Users table exists in SQLite
    sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Users'")
    if not sqlite_cursor.fetchone():
        print("❌ No Users table found in SQLite")
        sqlite_conn.close()
        return
    
    # Get all users from SQLite
    sqlite_cursor.execute("SELECT Id, Name, Email, PasswordHash, Role, CreatedAt, IsActive FROM Users")
    sqlite_users = sqlite_cursor.fetchall()
    sqlite_conn.close()
    
    if not sqlite_users:
        print("⚠️ No users found in SQLite")
        return
    
    print(f"📋 Found {len(sqlite_users)} users in SQLite")
    
    # Step 2: Connect to MySQL
    print("\n📂 Connecting to MySQL...")
    mysql_conn = get_mysql_connection()
    if mysql_conn is None:
        print("❌ Could not connect to MySQL")
        return
    
    mysql_cursor = mysql_conn.cursor()
    
    # Step 3: Migrate each user
    print("\n🔄 Migrating users to MySQL...")
    migrated_count = 0
    skipped_count = 0
    
    for user in sqlite_users:
        user_id = user[0]
        name = user[1]
        email = user[2]
        password_hash = user[3]
        role = user[4] if user[4] else 'User'
        created_at = user[5] if user[5] else datetime.now().isoformat()
        is_active = user[6] if user[6] is not None else 1
        
        try:
            # Check if user already exists in MySQL
            mysql_cursor.execute("SELECT Email FROM Users WHERE Email = %s", (email,))
            if mysql_cursor.fetchone():
                print(f"  ⏭️ Skipping {email} (already exists in MySQL)")
                skipped_count += 1
                continue
            
            # Insert user into MySQL
            mysql_cursor.execute("""
                INSERT INTO Users (Id, Email, Name, PasswordHash, Role, CreatedAt, IsActive)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (user_id, email, name, password_hash, role, created_at, is_active))
            
            print(f"  ✅ Migrated: {name} ({email})")
            migrated_count += 1
            
        except mysql.connector.Error as e:
            print(f"  ❌ Failed to migrate {email}: {e}")
    
    # Step 4: Commit and close
    mysql_conn.commit()
    mysql_conn.close()
    
    # Step 5: Show results
    print("\n" + "=" * 60)
    print("✅ MIGRATION COMPLETE!")
    print("=" * 60)
    print(f"📊 Users migrated: {migrated_count}")
    print(f"📊 Users skipped: {skipped_count}")
    print(f"📊 Total users in SQLite: {len(sqlite_users)}")
    
    # Show users in MySQL
    print("\n📋 Users now in MySQL:")
    mysql_conn = get_mysql_connection()
    if mysql_conn:
        mysql_cursor = mysql_conn.cursor()
        mysql_cursor.execute("SELECT Name, Email, Role FROM Users ORDER BY CreatedAt DESC")
        mysql_users = mysql_cursor.fetchall()
        for user in mysql_users:
            print(f"  👤 {user[0]} ({user[1]}) - Role: {user[2]}")
        mysql_conn.close()

if __name__ == "__main__":
    migrate_users()