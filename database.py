# database.py - SQLite Version for Streamlit Cloud

import sqlite3
import json
from datetime import datetime
import uuid
import hashlib
import os
import streamlit as st

# ============================================
# DATABASE SETUP - SQLite
# ============================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "skillbridge.db")

def get_connection():
    """Connect to SQLite database"""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        print(f"❌ Database error: {e}")
        return None

# ============================================
# AUTO-CREATE TABLES WHEN APP STARTS
# ============================================

def create_tables():
    """Create all tables if they don't exist"""
    print("🔄 Creating tables...")
    
    conn = get_connection()
    if conn is None:
        print("❌ Could not connect to database")
        return
    
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            Id TEXT PRIMARY KEY,
            Email TEXT UNIQUE NOT NULL,
            Name TEXT NOT NULL,
            PasswordHash TEXT NOT NULL,
            Role TEXT DEFAULT 'User',
            CreatedAt TEXT NOT NULL,
            IsActive INTEGER DEFAULT 1
        )
    ''')
    
    # Analyses table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Analyses (
            Id TEXT PRIMARY KEY,
            UserId TEXT NOT NULL,
            ResumeText TEXT,
            JobTitle TEXT,
            JobDescription TEXT,
            AtsScore INTEGER,
            SkillsHave TEXT,
            SkillsNeed TEXT,
            CreatedAt TEXT NOT NULL,
            FOREIGN KEY (UserId) REFERENCES Users(Id) ON DELETE CASCADE
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Database created successfully!")

# Create tables immediately when app starts
create_tables()

# ============================================
# CREATE DEFAULT ADMIN USER
# ============================================

def create_admin_user():
    """Create default admin user if not exists"""
    conn = get_connection()
    if conn is None:
        return
    
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Users WHERE Role = 'Admin'")
    count = cursor.fetchone()[0]
    
    if count == 0:
        print("👤 Creating default admin user...")
        user_id = str(uuid.uuid4())[:8]
        now = datetime.now().isoformat()
        password_hash = hashlib.sha256("admin123".encode()).hexdigest()
        
        cursor.execute("""
            INSERT INTO Users (Id, Email, Name, PasswordHash, Role, CreatedAt, IsActive)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (user_id, "admin@skillbridge.com", "Admin User", password_hash, "Admin", now, 1))
        
        conn.commit()
        print("✅ Default admin created: admin@skillbridge.com / admin123")
    
    conn.close()

# Create admin user immediately
create_admin_user()

# ============================================
# PASSWORD HASHING
# ============================================

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ============================================
# USER FUNCTIONS
# ============================================

def register_user(name, email, password):
    """Register a new user"""
    try:
        conn = get_connection()
        if conn is None:
            return None, "Database connection failed"
        
        cursor = conn.cursor()
        
        cursor.execute("SELECT Email FROM Users WHERE Email = ?", (email,))
        if cursor.fetchone():
            conn.close()
            return None, "Email already registered"
        
        user_id = str(uuid.uuid4())[:8]
        now = datetime.now().isoformat()
        hashed = hash_password(password)
        
        cursor.execute("""
            INSERT INTO Users (Id, Email, Name, PasswordHash, Role, CreatedAt, IsActive)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (user_id, email, name, hashed, 'User', now, 1))
        
        conn.commit()
        conn.close()
        print(f"✅ User registered: {email}")
        return user_id, "Registration successful!"
        
    except sqlite3.IntegrityError:
        return None, "Email already registered"
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return None, str(e)

def login_user(email, password):
    """Login a user"""
    try:
        conn = get_connection()
        if conn is None:
            return None, "Database connection failed"
        
        cursor = conn.cursor()
        hashed = hash_password(password)
        
        cursor.execute("""
            SELECT Id, Name, Email FROM Users 
            WHERE Email = ? AND PasswordHash = ? AND IsActive = 1
        """, (email, hashed))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            print(f"✅ Login successful: {email}")
            return result[0], "Login successful!"
        else:
            print(f"❌ Login failed: {email}")
            return None, "Invalid credentials"
            
    except Exception as e:
        print(f"❌ Login error: {e}")
        return None, str(e)

def is_admin(user_id):
    """Check if a user is an admin"""
    try:
        conn = get_connection()
        if conn is None:
            return False
        
        cursor = conn.cursor()
        cursor.execute("SELECT Role FROM Users WHERE Id = ?", (user_id,))
        result = cursor.fetchone()
        conn.close()
        
        if result and result[0] == 'Admin':
            return True
        return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def get_user_by_id(user_id):
    """Get user by ID"""
    try:
        conn = get_connection()
        if conn is None:
            return None
        
        cursor = conn.cursor()
        cursor.execute("SELECT Id, Name, Email, Role FROM Users WHERE Id = ?", (user_id,))
        result = cursor.fetchone()
        conn.close()
        return result
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def get_all_users():
    """Get all users"""
    try:
        conn = get_connection()
        if conn is None:
            return []
        
        cursor = conn.cursor()
        cursor.execute("SELECT Id, Name, Email, Role, CreatedAt, IsActive FROM Users ORDER BY CreatedAt DESC")
        results = cursor.fetchall()
        conn.close()
        return [tuple(row) for row in results]
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

def get_all_users_admin():
    """Get all users with full details (Admin only)"""
    try:
        conn = get_connection()
        if conn is None:
            return []
        
        cursor = conn.cursor()
        cursor.execute("SELECT Id, Name, Email, Role, CreatedAt, IsActive FROM Users ORDER BY CreatedAt DESC")
        results = cursor.fetchall()
        conn.close()
        return [tuple(row) for row in results]
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

def update_user_role_admin(user_id, new_role):
    """Update user role (Admin only)"""
    try:
        conn = get_connection()
        if conn is None:
            return False
        
        cursor = conn.cursor()
        cursor.execute("UPDATE Users SET Role = ? WHERE Id = ?", (new_role, user_id))
        conn.commit()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def delete_user_admin(user_id):
    """Delete a user (Admin only)"""
    try:
        conn = get_connection()
        if conn is None:
            return False
        
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Users WHERE Id = ?", (user_id,))
        conn.commit()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

# ============================================
# ANALYSIS FUNCTIONS
# ============================================

def save_analysis(user_id, result, resume_text, job_description):
    """Save analysis results to database"""
    try:
        conn = get_connection()
        if conn is None:
            return None
        
        cursor = conn.cursor()
        
        analysis_id = str(uuid.uuid4())[:8]
        now = datetime.now().isoformat()
        
        job_title = result.get("job_title", "Software Engineer")
        ats_score = result.get("ats_score", 0)
        skills_have = json.dumps(result.get("skills_have", []))
        skills_need = json.dumps(result.get("skills_need", []))
        
        cursor.execute("""
            INSERT INTO Analyses (
                Id, UserId, ResumeText, JobTitle, JobDescription, AtsScore,
                SkillsHave, SkillsNeed, CreatedAt
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            analysis_id, user_id, resume_text[:500], job_title, 
            job_description[:500], ats_score, skills_have, skills_need, now
        ))
        
        conn.commit()
        conn.close()
        print(f"✅ Analysis saved: {analysis_id}")
        return analysis_id
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def get_user_analyses(user_id):
    """Get all analyses for a user"""
    try:
        conn = get_connection()
        if conn is None:
            return []
        
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM Analyses 
            WHERE UserId = ? 
            ORDER BY CreatedAt DESC
        """, (user_id,))
        
        results = cursor.fetchall()
        conn.close()
        return [tuple(row) for row in results]
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

# ============================================
# STATISTICS FUNCTIONS
# ============================================

def get_user_statistics(user_id):
    """Get statistics for a user"""
    try:
        conn = get_connection()
        if conn is None:
            return {
                "total_analyses": 0,
                "avg_score": 0,
                "jobs_matched": 0,
                "progress": "Beginner"
            }
        
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM Analyses WHERE UserId = ?", (user_id,))
        total = cursor.fetchone()[0]
        
        cursor.execute("SELECT AVG(AtsScore) FROM Analyses WHERE UserId = ?", (user_id,))
        avg_result = cursor.fetchone()[0]
        avg_score = round(avg_result, 0) if avg_result else 0
        
        cursor.execute("SELECT COUNT(DISTINCT JobTitle) FROM Analyses WHERE UserId = ?", (user_id,))
        jobs_matched = cursor.fetchone()[0]
        
        if total == 0:
            progress = "Beginner"
        elif total < 3:
            progress = "Getting Started"
        elif total < 6:
            progress = "Building Skills"
        elif avg_score >= 70 and total >= 5:
            progress = "Advanced"
        else:
            progress = "Intermediate"
        
        conn.close()
        
        return {
            "total_analyses": total,
            "avg_score": avg_score,
            "jobs_matched": jobs_matched,
            "progress": progress
        }
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return {
            "total_analyses": 0,
            "avg_score": 0,
            "jobs_matched": 0,
            "progress": "Beginner"
        }

def get_system_stats_admin():
    """Get system statistics (Admin only)"""
    try:
        conn = get_connection()
        if conn is None:
            return {}
        
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM Users")
        total_users = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM Analyses")
        total_analyses = cursor.fetchone()[0]
        
        cursor.execute("SELECT AVG(AtsScore) FROM Analyses")
        avg_result = cursor.fetchone()[0]
        avg_score = round(avg_result, 0) if avg_result else 0
        
        cursor.execute("SELECT COUNT(*) FROM Users WHERE IsActive = 1")
        active_users = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM Users WHERE Role = 'Admin'")
        total_admins = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            "total_users": total_users,
            "total_analyses": total_analyses,
            "avg_score": avg_score,
            "active_users": active_users,
            "total_admins": total_admins
        }
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return {}
