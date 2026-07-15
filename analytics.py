# analytics.py - Analytics Dashboard for SkillBridge

import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, timedelta

# ============================================
# DATABASE CONNECTION
# ============================================

def get_connection():
    """Connect to SQLite database"""
    try:
        conn = sqlite3.connect("skillbridge.db")
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        print(f"❌ Database error: {e}")
        return None

# ============================================
# ANALYTICS FUNCTIONS
# ============================================

def get_overview_stats():
    """Get overview statistics"""
    conn = get_connection()
    if conn is None:
        return {}
    
    cursor = conn.cursor()
    
    # Total users
    cursor.execute("SELECT COUNT(*) FROM Users")
    total_users = cursor.fetchone()[0]
    
    # Total analyses
    cursor.execute("SELECT COUNT(*) FROM Analyses")
    total_analyses = cursor.fetchone()[0]
    
    # Average ATS score
    cursor.execute("SELECT AVG(AtsScore) FROM Analyses")
    avg_result = cursor.fetchone()[0]
    avg_score = round(avg_result, 0) if avg_result else 0
    
    # Users in last 7 days
    week_ago = (datetime.now() - timedelta(days=7)).isoformat()
    cursor.execute("SELECT COUNT(*) FROM Users WHERE CreatedAt > ?", (week_ago,))
    new_users_week = cursor.fetchone()[0]
    
    # Analyses in last 7 days
    cursor.execute("SELECT COUNT(*) FROM Analyses WHERE CreatedAt > ?", (week_ago,))
    analyses_week = cursor.fetchone()[0]
    
    # Admin count
    cursor.execute("SELECT COUNT(*) FROM Users WHERE Role = 'Admin'")
    admin_count = cursor.fetchone()[0]
    
    conn.close()
    
    return {
        "total_users": total_users,
        "total_analyses": total_analyses,
        "avg_score": avg_score,
        "new_users_week": new_users_week,
        "analyses_week": analyses_week,
        "admin_count": admin_count
    }

def get_daily_activity():
    """Get daily activity for the last 30 days"""
    conn = get_connection()
    if conn is None:
        return [], []
    
    cursor = conn.cursor()
    
    # Daily registrations
    cursor.execute("""
        SELECT DATE(CreatedAt) as date, COUNT(*) as count
        FROM Users
        WHERE CreatedAt > datetime('now', '-30 days')
        GROUP BY DATE(CreatedAt)
        ORDER BY date ASC
    """)
    user_data = cursor.fetchall()
    
    # Daily analyses
    cursor.execute("""
        SELECT DATE(CreatedAt) as date, COUNT(*) as count
        FROM Analyses
        WHERE CreatedAt > datetime('now', '-30 days')
        GROUP BY DATE(CreatedAt)
        ORDER BY date ASC
    """)
    analysis_data = cursor.fetchall()
    
    conn.close()
    
    return user_data, analysis_data

def get_popular_job_titles():
    """Get most popular job titles from analyses"""
    conn = get_connection()
    if conn is None:
        return []
    
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT JobTitle, COUNT(*) as count
        FROM Analyses
        WHERE JobTitle IS NOT NULL AND JobTitle != ''
        GROUP BY JobTitle
        ORDER BY count DESC
        LIMIT 10
    """)
    job_data = cursor.fetchall()
    
    conn.close()
    return job_data

def get_ats_score_distribution():
    """Get distribution of ATS scores"""
    conn = get_connection()
    if conn is None:
        return []
    
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT AtsScore, COUNT(*) as count
        FROM Analyses
        WHERE AtsScore IS NOT NULL
        GROUP BY AtsScore
        ORDER BY AtsScore ASC
    """)
    score_data = cursor.fetchall()
    
    conn.close()
    return score_data

def get_user_growth():
    """Get user growth over time"""
    conn = get_connection()
    if conn is None:
        return []
    
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT DATE(CreatedAt) as date, COUNT(*) as total
        FROM Users
        GROUP BY DATE(CreatedAt)
        ORDER BY date ASC
    """)
    growth_data = cursor.fetchall()
    
    conn.close()
    return growth_data

def get_recent_activity(limit=10):
    """Get recent user activity"""
    conn = get_connection()
    if conn is None:
        return []
    
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            u.Name as user_name,
            u.Email as user_email,
            a.JobTitle,
            a.AtsScore,
            a.CreatedAt
        FROM Analyses a
        JOIN Users u ON a.UserId = u.Id
        ORDER BY a.CreatedAt DESC
        LIMIT ?
    """, (limit,))
    
    recent_data = cursor.fetchall()
    conn.close()
    return recent_data

def get_analyses_by_user():
    """Get number of analyses per user"""
    conn = get_connection()
    if conn is None:
        return []
    
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            u.Name as user_name,
            u.Email as user_email,
            COUNT(a.Id) as analysis_count
        FROM Users u
        LEFT JOIN Analyses a ON u.Id = a.UserId
        GROUP BY u.Id
        ORDER BY analysis_count DESC
        LIMIT 10
    """)
    user_analyses = cursor.fetchall()
    
    conn.close()
    return user_analyses

# ============================================
# ANALYTICS UI
# ============================================

def show_analytics_dashboard():
    """Display analytics dashboard (Admin only)"""
    
    # Check if user is admin
    if not st.session_state.user_id:
        st.error("❌ Please login first")
        return
    
    from database import is_admin
    if not is_admin(st.session_state.user_id):
        st.error("❌ Access Denied. Admin privileges required.")
        return
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); padding: 25px; border-radius: 20px; color: white; text-align: center; margin-bottom: 25px;">
        <h1 style="color: white;">📊 Analytics Dashboard</h1>
        <p style="color: rgba(255,255,255,0.9);">Track user activity and app performance</p>
    </div>
    """, unsafe_allow_html=True)
    
    # ============================================
    # OVERVIEW STATISTICS
    # ============================================
    st.subheader("📈 Overview")
    
    stats = get_overview_stats()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "👥 Total Users", 
            stats.get("total_users", 0),
            delta=f"+{stats.get('new_users_week', 0)} this week"
        )
    
    with col2:
        st.metric(
            "📄 Total Analyses", 
            stats.get("total_analyses", 0),
            delta=f"+{stats.get('analyses_week', 0)} this week"
        )
    
    with col3:
        st.metric("📈 Avg ATS Score", f"{stats.get('avg_score', 0)}%")
    
    with col4:
        st.metric("👑 Admins", stats.get("admin_count", 0))
    
    st.divider()
    
    # ============================================
    # DAILY ACTIVITY CHART
    # ============================================
    st.subheader("📊 Daily Activity (Last 30 Days)")
    
    user_data, analysis_data = get_daily_activity()
    
    if user_data or analysis_data:
        # Create DataFrames
        df_users = pd.DataFrame(user_data, columns=["Date", "Registrations"]) if user_data else pd.DataFrame()
        df_analyses = pd.DataFrame(analysis_data, columns=["Date", "Analyses"]) if analysis_data else pd.DataFrame()
        
        # Merge data for visualization
        if not df_users.empty and not df_analyses.empty:
            df_merged = pd.merge(df_users, df_analyses, on="Date", how="outer").fillna(0)
            st.line_chart(df_merged.set_index("Date"))
        elif not df_users.empty:
            st.line_chart(df_users.set_index("Date"))
        elif not df_analyses.empty:
            st.line_chart(df_analyses.set_index("Date"))
        
        # Show raw data
        if not df_users.empty:
            st.caption(f"📋 Total Registrations: {df_users['Registrations'].sum()}")
        if not df_analyses.empty:
            st.caption(f"📋 Total Analyses: {df_analyses['Analyses'].sum()}")
    else:
        st.info("No activity data available yet")
    
    st.divider()
    
    # ============================================
    # POPULAR JOB TITLES
    # ============================================
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔥 Most Common Job Titles")
        
        job_data = get_popular_job_titles()
        
        if job_data:
            for job in job_data:
                st.info(f"📌 **{job[0]}** - {job[1]} analyses")
        else:
            st.info("No job title data available")
    
    with col2:
        st.subheader("📊 ATS Score Distribution")
        
        score_data = get_ats_score_distribution()
        
        if score_data:
            df_scores = pd.DataFrame(score_data, columns=["Score", "Count"])
            st.dataframe(df_scores, use_container_width=True)
        else:
            st.info("No score data available")
    
    st.divider()
    
    # ============================================
    # USER ANALYSES
    # ============================================
    st.subheader("🏆 Top Users by Analyses")
    
    user_analyses = get_analyses_by_user()
    
    if user_analyses:
        for user in user_analyses[:5]:
            st.metric(
                f"👤 {user[0]}",
                f"{user[2]} analyses",
                help=f"Email: {user[1]}"
            )
    else:
        st.info("No user analysis data available")
    
    st.divider()
    
    # ============================================
    # RECENT ACTIVITY
    # ============================================
    st.subheader("🔄 Recent Activity")
    
    recent = get_recent_activity(10)
    
    if recent:
        for activity in recent:
            with st.container():
                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    st.markdown(f"👤 **{activity[0]}** analyzed *{activity[2]}*")
                with col2:
                    st.markdown(f"📊 Score: {activity[3]}%")
                with col3:
                    st.caption(f"📅 {activity[4][:16]}")
                st.divider()
    else:
        st.info("No recent activity")
    
    st.divider()
    
    # ============================================
    # EXPORT DATA
    # ============================================
    st.subheader("📤 Export Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📥 Export Users Data", use_container_width=True):
            conn = get_connection()
            if conn:
                df_users = pd.read_sql_query("SELECT Id, Name, Email, Role, CreatedAt FROM Users", conn)
                conn.close()
                st.download_button(
                    "Download CSV",
                    df_users.to_csv(index=False),
                    file_name="users_data.csv",
                    mime="text/csv"
                )
    
    with col2:
        if st.button("📥 Export Analyses Data", use_container_width=True):
            conn = get_connection()
            if conn:
                df_analyses = pd.read_sql_query("SELECT Id, UserId, JobTitle, AtsScore, CreatedAt FROM Analyses", conn)
                conn.close()
                st.download_button(
                    "Download CSV",
                    df_analyses.to_csv(index=False),
                    file_name="analyses_data.csv",
                    mime="text/csv"
                )