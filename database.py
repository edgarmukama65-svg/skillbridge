# database.py - MySQL Version with Email Marketing

import mysql.connector
import json
from datetime import datetime
import uuid
import hashlib
import traceback

# ============================================
# IMPORT EMAIL SERVICE
# ============================================

from email_service import send_welcome_email

# ============================================
# DATABASE CONNECTION - MySQL
# ============================================

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = ""
DB_NAME = "skillbridge"

def get_connection():
    """Connect to MySQL database"""
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return conn
    except mysql.connector.Error as e:
        print(f"❌ MySQL Error: {e}")
        return None

# ============================================
# PASSWORD HASHING
# ============================================

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ============================================
# USER FUNCTIONS - WITH EMAIL
# ============================================

def register_user(name, email, password):
    """
    Register a new user - AUTOMATICALLY ADDS TO MYSQL DATABASE
    AND SENDS WELCOME EMAIL
    """
    try:
        print(f"🔄 Registering user: {name} ({email})")
        
        conn = get_connection()
        if conn is None:
            return None, "Database connection failed"
        
        cursor = conn.cursor()
        
        # Check if user exists
        cursor.execute("SELECT Email FROM Users WHERE Email = %s", (email,))
        if cursor.fetchone():
            conn.close()
            return None, "Email already registered"
        
        user_id = str(uuid.uuid4())[:8]
        now = datetime.now().isoformat()
        hashed = hash_password(password)
        
        cursor.execute("""
            INSERT INTO Users (Id, Email, Name, PasswordHash, Role, CreatedAt, IsActive)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (user_id, email, name, hashed, 'User', now, 1))
        
        conn.commit()
        conn.close()
        
        print(f"✅ User registered: {email}")
        
        # ============================================
        # SEND WELCOME EMAIL
        # ============================================
        if user_id:
            try:
                send_welcome_email(name, email)
                print(f"📧 Welcome email sent to {email}")
            except Exception as e:
                print(f"⚠️ Could not send welcome email: {e}")
        
        return user_id, "Registration successful!"
        
    except mysql.connector.IntegrityError as e:
        print(f"❌ Integrity Error: {e}")
        return None, "Email already registered"
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return None, str(e)

def login_user(email, password):
    """Login a user"""
    try:
        print(f"🔄 Login attempt: {email}")
        
        conn = get_connection()
        if conn is None:
            return None, "Database connection failed"
        
        cursor = conn.cursor()
        hashed = hash_password(password)
        
        cursor.execute("""
            SELECT Id, Name, Email FROM Users 
            WHERE Email = %s AND PasswordHash = %s AND IsActive = 1
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
        cursor.execute("SELECT Role FROM Users WHERE Id = %s", (user_id,))
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
        cursor.execute("SELECT Id, Name, Email, Role FROM Users WHERE Id = %s", (user_id,))
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
        return results
        
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
        return results
        
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
        cursor.execute("UPDATE Users SET Role = %s WHERE Id = %s", (new_role, user_id))
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
        cursor.execute("DELETE FROM Users WHERE Id = %s", (user_id,))
        conn.commit()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

# ============================================
# ANALYSIS FUNCTIONS - MYSQL VERSION
# ============================================

def save_analysis(user_id, result, resume_text, job_description):
    """
    Save complete analysis results to MySQL database
    Including: Analyses, Missing_Skills, Roadmap_Steps, Resume_Tips
    """
    try:
        print(f"🔄 Saving complete analysis for user: {user_id}")
        
        conn = get_connection()
        if conn is None:
            print("❌ Database connection failed!")
            return None
        
        cursor = conn.cursor()
        
        # Check if user exists
        cursor.execute("SELECT Id FROM Users WHERE Id = %s", (user_id,))
        if not cursor.fetchone():
            print(f"❌ User {user_id} does not exist!")
            conn.close()
            return None
        
        # Generate IDs and timestamps
        analysis_id = str(uuid.uuid4())[:8]
        now = datetime.now().isoformat()
        
        # Extract data from result
        job_title = result.get("job_title", "Software Engineer")
        ats_score = result.get("ats_score", 0)
        skills_have = json.dumps(result.get("skills_have", []))
        skills_need = json.dumps(result.get("skills_need", []))
        
        # Step 1: Save to Analyses table
        cursor.execute("""
            INSERT INTO Analyses (
                Id, UserId, ResumeText, JobTitle, JobDescription, AtsScore,
                SkillsHave, SkillsNeed, CreatedAt
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            analysis_id, user_id, resume_text[:500], job_title, 
            job_description[:500], ats_score, skills_have, skills_need, now
        ))
        print(f"✅ Analysis saved: {analysis_id}")
        
        # Step 2: Save Missing Skills
        missing_skills = result.get("skills_missing", [])
        for skill in missing_skills:
            skill_id = str(uuid.uuid4())[:8]
            cursor.execute("""
                INSERT INTO Missing_Skills (Id, AnalysisId, SkillName, Importance, CreatedAt)
                VALUES (%s, %s, %s, %s, %s)
            """, (skill_id, analysis_id, skill, "High", now))
            print(f"  ✅ Missing skill saved: {skill}")
        
        # Step 3: Save Roadmap Steps
        roadmap = result.get("learning_roadmap", [])
        for i, step in enumerate(roadmap, 1):
            step_id = str(uuid.uuid4())[:8]
            cursor.execute("""
                INSERT INTO Roadmap_Steps (Id, AnalysisId, StepOrder, ActionItem, CreatedAt)
                VALUES (%s, %s, %s, %s, %s)
            """, (step_id, analysis_id, i, step[:500], now))
            print(f"  ✅ Roadmap step saved: {step[:50]}...")
        
        # Step 4: Save Resume Tips
        tips = result.get("resume_tips", [])
        for i, tip in enumerate(tips, 1):
            tip_id = str(uuid.uuid4())[:8]
            cursor.execute("""
                INSERT INTO Resume_Tips (Id, AnalysisId, TipOrder, TipText, Category, CreatedAt)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (tip_id, analysis_id, i, tip[:500], "General", now))
            print(f"  ✅ Resume tip saved: {tip[:50]}...")
        
        conn.commit()
        conn.close()
        
        print(f"✅ Complete analysis saved to MySQL: {analysis_id}")
        return analysis_id
        
    except mysql.connector.Error as e:
        print(f"❌ MySQL Error: {e}")
        print(f"Error details: {traceback.format_exc()}")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"Error details: {traceback.format_exc()}")
        return None

def get_user_analyses(user_id):
    """
    Get all analyses for a user from MySQL
    """
    try:
        conn = get_connection()
        if conn is None:
            return []
        
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM Analyses 
            WHERE UserId = %s 
            ORDER BY CreatedAt DESC
        """, (user_id,))
        
        results = cursor.fetchall()
        conn.close()
        return results
        
    except mysql.connector.Error as e:
        print(f"❌ MySQL Error: {e}")
        return []

def get_analysis_details(analysis_id):
    """
    Get complete analysis details including missing skills, roadmap, tips
    """
    try:
        conn = get_connection()
        if conn is None:
            return None
        
        cursor = conn.cursor()
        
        # Get main analysis
        cursor.execute("SELECT * FROM Analyses WHERE Id = %s", (analysis_id,))
        analysis = cursor.fetchone()
        
        if not analysis:
            conn.close()
            return None
        
        # Get missing skills
        cursor.execute("SELECT * FROM Missing_Skills WHERE AnalysisId = %s", (analysis_id,))
        missing_skills = cursor.fetchall()
        
        # Get roadmap steps
        cursor.execute("SELECT * FROM Roadmap_Steps WHERE AnalysisId = %s ORDER BY StepOrder", (analysis_id,))
        roadmap_steps = cursor.fetchall()
        
        # Get resume tips
        cursor.execute("SELECT * FROM Resume_Tips WHERE AnalysisId = %s ORDER BY TipOrder", (analysis_id,))
        resume_tips = cursor.fetchall()
        
        conn.close()
        
        return {
            "analysis": analysis,
            "missing_skills": missing_skills,
            "roadmap_steps": roadmap_steps,
            "resume_tips": resume_tips
        }
        
    except mysql.connector.Error as e:
        print(f"❌ MySQL Error: {e}")
        return None

# ============================================
# STATISTICS FUNCTIONS - MYSQL VERSION
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
        
        cursor.execute("SELECT COUNT(*) FROM Analyses WHERE UserId = %s", (user_id,))
        total = cursor.fetchone()[0]
        
        cursor.execute("SELECT AVG(AtsScore) FROM Analyses WHERE UserId = %s", (user_id,))
        avg_result = cursor.fetchone()[0]
        avg_score = round(avg_result, 0) if avg_result else 0
        
        cursor.execute("SELECT COUNT(DISTINCT JobTitle) FROM Analyses WHERE UserId = %s", (user_id,))
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

# ============================================
# DATABASE SETUP
# ============================================

def setup_database():
    """Complete database setup"""
    print("🔄 Setting up SkillBridge MySQL database...")
    print("📁 Database: skillbridge on MySQL")
    
    conn = get_connection()
    if conn is None:
        print("❌ Could not connect to MySQL. Make sure XAMPP is running.")
        return
    
    cursor = conn.cursor()
    
    # Check if admin user exists
    cursor.execute("SELECT COUNT(*) FROM Users WHERE Role = 'Admin'")
    count = cursor.fetchone()[0]
    conn.close()
    
    if count == 0:
        print("👤 Creating default admin user...")
        admin_id, msg = register_user("Admin User", "admin@skillbridge.com", "admin123")
        if admin_id:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE Users SET Role = 'Admin' WHERE Id = %s", (admin_id,))
            conn.commit()
            conn.close()
            print("✅ Default admin created: admin@skillbridge.com / admin123")
    
    print("✅ Database setup complete!")

if __name__ == "__main__":
    setup_database()