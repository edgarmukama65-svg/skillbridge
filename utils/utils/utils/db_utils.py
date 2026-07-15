# utils/db_utils.py - Database operations for SkillBridge

import sqlite3
import uuid
from datetime import datetime
import json

DB_PATH = "database/skillbridge.db"

def get_db_connection():
    """Creates a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    """Creates all tables if they don't exist."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analyses (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            resume_text TEXT NOT NULL,
            job_description TEXT NOT NULL,
            ats_score INTEGER NOT NULL,
            skills_have TEXT NOT NULL,
            skills_need TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS missing_skills (
            id TEXT PRIMARY KEY,
            analysis_id TEXT NOT NULL,
            skill_name TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    
    conn.commit()
    conn.close()

def save_analysis(user_id, resume_text, job_description, ats_score, skills_have, skills_need, missing_skills):
    """Saves an analysis to the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    analysis_id = str(uuid.uuid4())
    created_at = datetime.now().isoformat()
    
    cursor.execute("""
        INSERT INTO analyses (id, user_id, resume_text, job_description, ats_score, skills_have, skills_need, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (analysis_id, user_id, resume_text, job_description, ats_score, json.dumps(skills_have), json.dumps(skills_need), created_at))
    
    for skill in missing_skills:
        skill_id = str(uuid.uuid4())
        cursor.execute("""
            INSERT INTO missing_skills (id, analysis_id, skill_name, created_at)
            VALUES (?, ?, ?, ?)
        """, (skill_id, analysis_id, skill, created_at))
    
    conn.commit()
    conn.close()
    return analysis_id