# app.py - SkillBridge Complete Application
# All Features: Authentication, Admin Panel, Analytics, Resume Builder,
# Cover Letter Generator, Pricing, Password Reset, Mobile Responsive,
# Payment, PDF Export, Advanced Algorithm, Job Recommendations (with Upload),
# Salary Estimator (with Upload), Interview Questions

import streamlit as st
import PyPDF2
import random
import pandas as pd
import json
from database import (
    register_user, login_user, save_analysis, get_user_analyses,
    get_user_statistics, is_admin, get_user_by_id
)
from algorithms import analyze_skills_advanced
from datetime import datetime
from report_generator import generate_analysis_report
from job_recommendations import recommend_jobs
from salary_estimator import estimate_salary
from interview_questions import generate_questions
import urllib.parse

# ============================================
# PAGE CONFIGURATION
# ============================================
st.set_page_config(
    page_title="SkillBridge - Your AI Career Coach",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# SESSION STATE
# ============================================
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "user_email" not in st.session_state:
    st.session_state.user_email = ""
if "analysis_history" not in st.session_state:
    st.session_state.analysis_history = []
if "show_reset" not in st.session_state:
    st.session_state.show_reset = False
if "show_new_password" not in st.session_state:
    st.session_state.show_new_password = False
if "reset_email" not in st.session_state:
    st.session_state.reset_email = ""

# ============================================
# PASSWORD RESET TOKEN HANDLER
# ============================================
query_params = st.query_params

if "reset_token" in query_params:
    token = query_params["reset_token"]
    from reset_password import verify_reset_token
    email = verify_reset_token(token)
    if email:
        st.session_state.reset_email = email
        st.session_state.show_new_password = True
        st.success(f"✅ Token verified! Reset password for {email}")
    else:
        st.error("❌ Invalid or expired reset token")

# ============================================
# CUSTOM CSS - PROFESSIONAL & MOBILE RESPONSIVE
# ============================================
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    }
    .css-1d391kg .stMarkdown, .css-1d391kg .stTextInput, .css-1d391kg .stButton {
        color: white !important;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #1a1a2e !important;
        font-weight: 700 !important;
    }
    
    /* Gradient buttons */
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        border: none !important;
        border-radius: 30px !important;
        padding: 12px 30px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        transform: scale(1.05);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
    }
    
    /* Metrics */
    .stMetric {
        background: white;
        border-radius: 15px;
        padding: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }
    
    /* Mobile Responsive */
    @media (max-width: 768px) {
        .row-widget.stColumns {
            flex-direction: column !important;
        }
        .stButton button {
            width: 100% !important;
        }
        h1 {
            font-size: 28px !important;
        }
        h2 {
            font-size: 22px !important;
        }
        h3 {
            font-size: 18px !important;
        }
        .stMetric {
            padding: 10px !important;
            margin: 5px 0 !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# SIDEBAR - AUTHENTICATION & NAVIGATION
# ============================================
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h1 style="font-size: 60px; margin: 0;">🚀</h1>
        <h2 style="color: white; margin: 0;">SkillBridge</h2>
        <p style="color: #aaa; font-size: 14px;">Your AI Career Coach</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # ============================================
    # AUTHENTICATION
    # ============================================
    if st.session_state.user_id:
        if is_admin(st.session_state.user_id):
            st.success(f"👑 **{st.session_state.user_name}** (Admin)")
        else:
            st.success(f"✅ **{st.session_state.user_name}**")
        st.caption(f"📧 {st.session_state.user_email}")
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.user_id = None
            st.session_state.user_name = ""
            st.session_state.user_email = ""
            st.session_state.show_reset = False
            st.session_state.show_new_password = False
            st.rerun()
    else:
        tab1, tab2, tab3 = st.tabs(["🔐 Login", "📝 Register", "👑 Admin"])
        
        with tab1:
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_pass")
            
            col1, col2 = st.columns([2, 1])
            with col1:
                if st.button("Login", use_container_width=True, key="login_btn"):
                    user_id, msg = login_user(email, password)
                    if user_id:
                        st.session_state.user_id = user_id
                        st.session_state.user_email = email
                        st.session_state.user_name = email.split("@")[0]
                        st.success("✅ Login successful!")
                        st.rerun()
                    else:
                        st.error(f"❌ {msg}")
            
            with col2:
                if st.button("🔒 Forgot?", use_container_width=True):
                    st.session_state.show_reset = True
                    st.rerun()
        
        with tab2:
            name = st.text_input("Full Name", key="reg_name")
            email = st.text_input("Email", key="reg_email")
            password = st.text_input("Password", type="password", key="reg_pass")
            confirm = st.text_input("Confirm Password", type="password", key="reg_confirm")
            
            if st.button("Register", use_container_width=True, key="reg_btn"):
                if not name or not email or not password:
                    st.warning("Please fill all fields")
                elif password != confirm:
                    st.error("Passwords don't match")
                elif len(password) < 4:
                    st.error("Password too short")
                else:
                    user_id, msg = register_user(name, email, password)
                    if user_id:
                        st.session_state.user_id = user_id
                        st.session_state.user_email = email
                        st.session_state.user_name = name
                        st.success(f"✅ Welcome {name}!")
                        st.rerun()
                    else:
                        st.error(f"❌ {msg}")
        
        with tab3:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #667eea, #764ba2); padding: 15px; border-radius: 10px; color: white; text-align: center; margin-bottom: 15px;">
                <h4 style="color: white; margin: 0;">👑 Admin Access</h4>
                <p style="color: rgba(255,255,255,0.9); font-size: 12px; margin: 5px 0 0 0;">Restricted to authorized personnel only</p>
            </div>
            """, unsafe_allow_html=True)
            
            admin_email = st.text_input("Admin Email", placeholder="admin@skillbridge.com", key="admin_email")
            admin_pass = st.text_input("Admin Password", type="password", placeholder="Enter admin password", key="admin_pass")
            
            if st.button("👑 Admin Login", use_container_width=True, key="admin_btn"):
                if admin_email and admin_pass:
                    user_id, msg = login_user(admin_email, admin_pass)
                    if user_id:
                        if is_admin(user_id):
                            user = get_user_by_id(user_id)
                            user_name = user[1] if user else "Admin"
                            
                            st.session_state.user_id = user_id
                            st.session_state.user_email = admin_email
                            st.session_state.user_name = user_name
                            st.success("✅ Admin login successful!")
                            st.rerun()
                        else:
                            st.error("❌ This account is not an admin!")
                    else:
                        st.error(f"❌ {msg}")
                else:
                    st.warning("⚠️ Please enter email and password")
    
    st.divider()
    
    # ============================================
    # NAVIGATION - UPDATED WITH ALL FEATURES
    # ============================================
    st.header("📱 Navigation")
    
    if st.session_state.user_id and is_admin(st.session_state.user_id):
        nav_options = ["🏠 Home", "👑 Admin Panel", "📊 Analytics", "📄 Resume Builder", "📝 Cover Letter", "💰 Pricing", "💳 Payment", "💼 Jobs", "💰 Salary Estimator", "🎤 Interview Questions"]
    else:
        nav_options = ["🏠 Home", "📄 Resume Builder", "📝 Cover Letter", "💰 Pricing", "💳 Payment", "💼 Jobs", "💰 Salary Estimator", "🎤 Interview Questions"]
    
    selected_nav = st.radio("Go to", nav_options, index=0)

# ============================================
# PASSWORD RESET PAGE
# ============================================
if st.session_state.get("show_reset", False):
    from reset_password import show_password_reset
    show_password_reset()
    st.stop()

# ============================================
# PDF EXTRACTION
# ============================================

def extract_text(pdf_file):
    try:
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text.strip(), None
    except Exception as e:
        return None, str(e)

# ============================================
# HOME PAGE
# ============================================
if selected_nav == "🏠 Home":
    st.title("🚀 SkillBridge")
    st.subheader("Your AI Career Coach - Find skill gaps and land your dream job")
    
    if st.session_state.user_id:
        stats = get_user_statistics(st.session_state.user_id)
        col1, col2, col3, col4 = st.columns(4)
        with col1: st.metric("📊 Total Analyses", stats["total_analyses"])
        with col2: st.metric("📈 Avg Score", f"{stats['avg_score']:.0f}%")
        with col3: st.metric("🎯 Jobs Matched", stats["jobs_matched"])
        with col4: st.metric("⭐ Progress", stats["progress"])
    
    st.divider()
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 20px; color: white; text-align: center; margin-bottom: 20px;">
        <h3 style="color: white;">🚀 Upload your resume and get instant feedback</h3>
        <p style="color: rgba(255,255,255,0.9);">Discover skill gaps and get a personalized learning roadmap</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
        job_desc = st.text_area("Paste job description here:", height=150)
        analyze_btn = st.button("🔍 Analyze My Skills", use_container_width=True)
    
    with col2:
        if analyze_btn:
            if not uploaded_file:
                st.error("❌ Please upload a PDF file")
            elif not job_desc:
                st.error("❌ Please paste a job description")
            else:
                with st.spinner("Analyzing your resume with advanced AI..."):
                    text, err = extract_text(uploaded_file)
                    if err:
                        st.error(f"❌ PDF error: {err}")
                    else:
                        st.success("✅ PDF text extracted successfully!")
                        
                        # ============================================
                        # USING ADVANCED ALGORITHM
                        # ============================================
                        result = analyze_skills_advanced(text, job_desc)
                        
                        if st.session_state.user_id:
                            analysis_id = save_analysis(st.session_state.user_id, result, text, job_desc)
                            if analysis_id:
                                st.success("✅ Results saved to database!")
                            else:
                                st.warning("⚠️ Results not saved to database")
                        
                        # Display Results
                        score = result.get("ats_score", 0)
                        job_title = result.get("job_title", "Software Engineer")
                        
                        st.markdown(f"### 🎯 Job Title Detected: **{job_title}**")
                        
                        st.markdown("### 📊 ATS Compatibility Score")
                        col1, col2, col3 = st.columns([2, 1, 1])
                        with col1:
                            if score >= 70:
                                st.progress(score/100, text=f"{score}% ✅ Strong Match")
                            elif score >= 50:
                                st.progress(score/100, text=f"{score}% ⚠️ Moderate Match")
                            else:
                                st.progress(score/100, text=f"{score}% ❌ Needs Work")
                        with col2:
                            st.metric("Score", f"{score}%")
                        with col3:
                            status = "✅ Strong" if score >= 70 else "⚠️ Moderate" if score >= 50 else "❌ Needs Work"
                            st.metric("Status", status)
                        
                        # Skill Categories
                        categories = result.get("skill_categories", {})
                        if categories:
                            st.markdown("### 📂 Skill Category Breakdown")
                            for category, data in categories.items():
                                found_count = data.get("found", 0)
                                needed_count = data.get("needed", 0)
                                col1, col2, col3 = st.columns([2, 1, 1])
                                with col1:
                                    st.markdown(f"**{category.title()}**")
                                with col2:
                                    st.markdown(f"✅ Found: {found_count}")
                                with col3:
                                    st.markdown(f"📌 Needed: {needed_count}")
                        
                        # Skills
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown("#### ✅ Skills You Have")
                            for skill in result.get("skills_have", []):
                                st.success(f"✅ {skill.title()}")
                        with col2:
                            st.markdown("#### 📌 Skills You Need")
                            for skill in result.get("skills_need", []):
                                st.warning(f"📌 {skill.title()}")
                        
                        # Missing Skills
                        st.markdown("#### 🚨 Missing Skills")
                        missing = result.get("skills_missing", [])
                        if missing:
                            for skill in missing:
                                st.error(f"🔴 **{skill.title()}** - Add this to your resume!")
                        else:
                            st.success("🎉 No missing skills found!")
                        
                        # Learning Roadmap
                        st.markdown("#### 📚 Personalized Learning Roadmap")
                        for i, step in enumerate(result.get("learning_roadmap", []), 1):
                            st.info(f"**Step {i}:** {step}")
                        
                        # Resume Tips
                        st.markdown("#### 💡 Resume Optimization Tips")
                        for i, tip in enumerate(result.get("resume_tips", []), 1):
                            st.info(f"**Tip {i}:** {tip}")
                        
                        # ============================================
                        # EXPORT PDF REPORT
                        # ============================================
                        st.divider()
                        st.subheader("📄 Export Report")
                        
                        if st.session_state.user_id:
                            user = get_user_by_id(st.session_state.user_id)
                            user_name = user[1] if user else "User"
                            
                            if st.button("📄 Generate PDF Report", use_container_width=True):
                                with st.spinner("Generating your professional PDF report..."):
                                    pdf_data = generate_analysis_report(
                                        result, text, job_desc, user_name
                                    )
                                    st.download_button(
                                        label="📥 Download PDF Report",
                                        data=pdf_data,
                                        file_name=f"SkillBridge_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                                        mime="application/pdf",
                                        use_container_width=True
                                    )
                        else:
                            st.info("🔓 Login to download your report")
    
    st.divider()
    st.markdown("### 📋 Your History")
    
    if st.session_state.user_id:
        history = get_user_analyses(st.session_state.user_id)
        if history:
            for h in history[:5]:
                try:
                    created_at = h[8] if len(h) > 8 else "No Date"
                    ats_score = h[5] if len(h) > 5 else 0
                    job_title = h[3] if len(h) > 3 else "Unknown"
                    
                    if created_at and created_at != "No Date":
                        date_short = created_at[:16].replace("T", " ") if len(created_at) > 16 else created_at
                    else:
                        date_short = "No Date"
                    
                    st.info(f"📅 {date_short} | Score: {ats_score}% | Job: {job_title}")
                except Exception as e:
                    st.warning(f"Error displaying analysis: {e}")
        else:
            st.info("No analyses yet. Run your first analysis!")
    else:
        st.info("🔓 Login to save and view your history!")

# ============================================
# ADMIN PANEL
# ============================================
elif selected_nav == "👑 Admin Panel":
    st.title("👑 Admin Dashboard")
    
    if not st.session_state.user_id:
        st.error("❌ Please login first")
    elif not is_admin(st.session_state.user_id):
        st.error("❌ Access Denied. Admin privileges required.")
    else:
        st.markdown(f"Welcome back, **{st.session_state.user_name}**!")
        
        st.header("📊 System Statistics")
        
        from database import get_system_stats_admin, get_all_users_admin, update_user_role_admin, delete_user_admin
        
        stats = get_system_stats_admin()
        
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1: st.metric("👥 Total Users", stats.get("total_users", 0))
        with col2: st.metric("📄 Total Analyses", stats.get("total_analyses", 0))
        with col3: st.metric("📈 Avg Score", f"{stats.get('avg_score', 0)}%")
        with col4: st.metric("🟢 Active Users", stats.get("active_users", 0))
        with col5: st.metric("👑 Admins", stats.get("total_admins", 0))
        
        st.divider()
        
        st.header("👥 User Management")
        
        users = get_all_users_admin()
        
        if users:
            df = pd.DataFrame(users, columns=["ID", "Name", "Email", "Role", "Created At", "Active"])
            st.dataframe(df, use_container_width=True)
            
            st.subheader("🛠️ User Actions")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                user_id = st.selectbox(
                    "Select User",
                    options=[u[0] for u in users],
                    format_func=lambda x: f"{x} - {next((u[1] for u in users if u[0] == x), '')}"
                )
            
            with col2:
                new_role = st.selectbox("New Role", ["User", "Admin"])
            
            with col3:
                if st.button("🔄 Update Role", use_container_width=True):
                    if update_user_role_admin(user_id, new_role):
                        st.success(f"✅ User role updated to {new_role}")
                        st.rerun()
                    else:
                        st.error("❌ Failed to update role")
            
            if st.button("🗑️ Delete Selected User", use_container_width=True):
                if st.session_state.user_id == user_id:
                    st.error("❌ Cannot delete yourself!")
                else:
                    if delete_user_admin(user_id):
                        st.success("✅ User deleted successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Failed to delete user")

# ============================================
# ANALYTICS DASHBOARD
# ============================================
elif selected_nav == "📊 Analytics":
    from analytics import show_analytics_dashboard
    show_analytics_dashboard()

# ============================================
# RESUME BUILDER
# ============================================
elif selected_nav == "📄 Resume Builder":
    st.title("📄 Professional Resume Builder")
    st.markdown("Create a professional resume in minutes")
    
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name", placeholder="John Doe")
        email = st.text_input("Email", placeholder="john@email.com")
        phone = st.text_input("Phone", placeholder="+1 234 567 890")
    with col2:
        location = st.text_input("Location", placeholder="New York, NY")
        skills = st.text_area("Skills (comma separated)", placeholder="Python, SQL, JavaScript, Docker")
        experience = st.text_area("Experience", placeholder="Software Engineer | Google | 2020-Present")
    
    if st.button("Generate Resume", use_container_width=True):
        if name and email:
            st.success("✅ Resume generated successfully!")
            resume_content = f"""Name: {name}
Email: {email}
Phone: {phone}
Location: {location}

Skills: {skills}

Experience:
{experience}
"""
            st.download_button(
                "📥 Download Resume",
                data=resume_content,
                file_name="resume.txt",
                mime="text/plain"
            )
        else:
            st.error("❌ Please fill in Name and Email")

# ============================================
# COVER LETTER GENERATOR
# ============================================
elif selected_nav == "📝 Cover Letter":
    st.title("📝 AI Cover Letter Generator")
    
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Your Name", placeholder="John Doe")
        job_title = st.text_input("Job Title", placeholder="Software Engineer")
    with col2:
        company = st.text_input("Company Name", placeholder="Google")
        skills_highlight = st.text_area("Key Skills", placeholder="Python, Leadership, Problem Solving")
    
    if st.button("Generate Cover Letter", use_container_width=True):
        if name and job_title and company:
            cover = f"""{name}

Dear Hiring Manager,

I am writing to express my strong interest in the {job_title} position at {company}.

With my skills in {skills_highlight}, I am confident that I would be a valuable addition to your team. I am passionate about delivering high-quality work and contributing to the success of {company}.

Thank you for considering my application. I look forward to the opportunity to discuss how my skills and experience align with the needs of {company}.

Sincerely,
{name}"""
            
            st.success("✅ Cover Letter Generated!")
            st.text(cover)
            st.download_button(
                "📥 Download Cover Letter",
                data=cover,
                file_name="cover_letter.txt",
                mime="text/plain"
            )
        else:
            st.error("❌ Please fill in Name, Job Title, and Company")

# ============================================
# PRICING PLANS
# ============================================
elif selected_nav == "💰 Pricing":
    st.title("💰 Choose Your Plan")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("""
        ### Free
        **$0** /month
        
        ✅ 5 analyses/month
        ✅ Basic ATS Score
        ✅ Community Support
        """)
    
    with col2:
        st.success("""
        ### ⭐ Pro
        **$9.99** /month
        
        ✅ Unlimited analyses
        ✅ Advanced AI Analysis
        ✅ Detailed Reports
        ✅ Email Support
        ✅ Resume Builder
        """)
    
    with col3:
        st.warning("""
        ### 🏢 Enterprise
        **$49.99** /month
        
        ✅ Team Management
        ✅ Career Coach Access
        ✅ API Access
        ✅ Dedicated Support
        ✅ Custom Solutions
        """)

# ============================================
# PAYMENT PAGE
# ============================================
elif selected_nav == "💳 Payment":
    from payment import show_payment_page, handle_payment_callback
    handle_payment_callback()
    show_payment_page()

# ============================================
# JOB RECOMMENDATIONS - WITH UPLOAD
# ============================================
elif selected_nav == "💼 Jobs":
    st.title("💼 Job Recommendations")
    st.subheader("Find jobs that match your skills")
    
    if st.session_state.user_id:
        # Check if user has existing skills
        history = get_user_analyses(st.session_state.user_id)
        all_skills = []
        
        for h in history[:10]:
            try:
                if len(h) > 7 and h[7]:
                    skills_have = json.loads(h[7])
                    if isinstance(skills_have, list):
                        all_skills.extend(skills_have)
            except:
                pass
        
        user_skills = list(set(all_skills))
        
        if user_skills:
            st.info(f"📋 Your Skills: {', '.join(user_skills[:10])}")
            
            if len(user_skills) > 10:
                st.caption(f"... and {len(user_skills) - 10} more skills")
            
            # Show existing recommendations
            with st.spinner("Finding jobs that match your skills..."):
                recommendations = recommend_jobs(user_skills, limit=5)
            
            if recommendations:
                st.success(f"✅ Found {len(recommendations)} job matches!")
                
                for i, job in enumerate(recommendations, 1):
                    with st.expander(f"{i}. {job['title']} at {job['company']} - {job['match_score']}% Match", expanded=(i==1)):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown(f"**📍 Location:** {job['location']}")
                            st.markdown(f"**💰 Salary:** {job['salary']}")
                            st.markdown(f"**🎯 Match Score:** {job['match_score']}%")
                        with col2:
                            st.markdown(f"**📊 Experience:** {job['experience_level']}")
                            st.markdown(f"**✅ Matched Skills:** {', '.join(job['matched_skills'])}")
                            if job['missing_skills']:
                                st.warning(f"**❌ Missing Skills:** {', '.join(job['missing_skills'])}")
                        
                        st.markdown(f"**📝 Description:** {job['description']}")
                        
                        if st.button(f"📧 Apply Now", key=f"apply_{i}"):
                            st.success(f"✅ Application started for {job['title']} at {job['company']}!")
            else:
                st.info("No job matches found. Upload a new resume to improve your profile.")
                
                # Upload section
                st.divider()
                st.subheader("📄 Upload a Resume to Find Jobs")
                
                col1, col2 = st.columns([1, 2])
                with col1:
                    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf", key="job_upload")
                with col2:
                    job_title_input = st.text_input("Job Title (Optional)", placeholder="e.g., Software Engineer")
                
                if st.button("🔍 Analyze Resume for Job Matches", use_container_width=True):
                    if uploaded_file:
                        with st.spinner("Analyzing your resume..."):
                            text, err = extract_text(uploaded_file)
                            if err:
                                st.error(f"❌ PDF error: {err}")
                            else:
                                st.success("✅ Resume analyzed successfully!")
                                
                                # Extract skills
                                result = analyze_skills_advanced(text, job_title_input or "Software Engineer")
                                skills_from_resume = result.get("skills_have", [])
                                
                                if skills_from_resume:
                                    st.info(f"📋 Skills Found: {', '.join(skills_from_resume)}")
                                    
                                    if st.session_state.user_id:
                                        analysis_id = save_analysis(st.session_state.user_id, result, text, job_title_input or "Software Engineer")
                                        if analysis_id:
                                            st.success("✅ Results saved to database!")
                                    
                                    recommendations = recommend_jobs(skills_from_resume, limit=5)
                                    
                                    if recommendations:
                                        st.success(f"✅ Found {len(recommendations)} job matches!")
                                        
                                        for i, job in enumerate(recommendations, 1):
                                            with st.expander(f"{i}. {job['title']} at {job['company']} - {job['match_score']}% Match", expanded=(i==1)):
                                                col1, col2 = st.columns(2)
                                                with col1:
                                                    st.markdown(f"**📍 Location:** {job['location']}")
                                                    st.markdown(f"**💰 Salary:** {job['salary']}")
                                                    st.markdown(f"**🎯 Match Score:** {job['match_score']}%")
                                                with col2:
                                                    st.markdown(f"**📊 Experience:** {job['experience_level']}")
                                                    st.markdown(f"**✅ Matched Skills:** {', '.join(job['matched_skills'])}")
                                                    if job['missing_skills']:
                                                        st.warning(f"**❌ Missing Skills:** {', '.join(job['missing_skills'])}")
                                                
                                                st.markdown(f"**📝 Description:** {job['description']}")
                                    else:
                                        st.info("No job matches found for your skills.")
                                else:
                                    st.warning("No skills were extracted from your resume.")
                    else:
                        st.error("❌ Please upload a PDF file.")
        else:
            # User has no skills - show upload
            st.info("📄 Upload your resume to discover job matches!")
            
            st.divider()
            st.subheader("📄 Upload a Resume to Find Jobs")
            
            col1, col2 = st.columns([1, 2])
            with col1:
                uploaded_file = st.file_uploader("Choose a PDF file", type="pdf", key="job_upload_first")
            with col2:
                job_title_input = st.text_input("Job Title (Optional)", placeholder="e.g., Software Engineer")
            
            if st.button("🔍 Analyze Resume for Job Matches", use_container_width=True):
                if uploaded_file:
                    with st.spinner("Analyzing your resume..."):
                        text, err = extract_text(uploaded_file)
                        if err:
                            st.error(f"❌ PDF error: {err}")
                        else:
                            st.success("✅ Resume analyzed successfully!")
                            
                            result = analyze_skills_advanced(text, job_title_input or "Software Engineer")
                            skills_from_resume = result.get("skills_have", [])
                            
                            if skills_from_resume:
                                st.info(f"📋 Skills Found: {', '.join(skills_from_resume)}")
                                
                                if st.session_state.user_id:
                                    analysis_id = save_analysis(st.session_state.user_id, result, text, job_title_input or "Software Engineer")
                                    if analysis_id:
                                        st.success("✅ Results saved to database!")
                                
                                recommendations = recommend_jobs(skills_from_resume, limit=5)
                                
                                if recommendations:
                                    st.success(f"✅ Found {len(recommendations)} job matches!")
                                    
                                    for i, job in enumerate(recommendations, 1):
                                        with st.expander(f"{i}. {job['title']} at {job['company']} - {job['match_score']}% Match", expanded=(i==1)):
                                            col1, col2 = st.columns(2)
                                            with col1:
                                                st.markdown(f"**📍 Location:** {job['location']}")
                                                st.markdown(f"**💰 Salary:** {job['salary']}")
                                                st.markdown(f"**🎯 Match Score:** {job['match_score']}%")
                                            with col2:
                                                st.markdown(f"**📊 Experience:** {job['experience_level']}")
                                                st.markdown(f"**✅ Matched Skills:** {', '.join(job['matched_skills'])}")
                                                if job['missing_skills']:
                                                    st.warning(f"**❌ Missing Skills:** {', '.join(job['missing_skills'])}")
                                            
                                            st.markdown(f"**📝 Description:** {job['description']}")
                                else:
                                    st.info("No job matches found for your skills.")
                            else:
                                st.warning("No skills were extracted from your resume.")
                else:
                    st.error("❌ Please upload a PDF file.")
    else:
        st.warning("🔓 Please login to see job recommendations")

# ============================================
# SALARY ESTIMATOR - WITH UPLOAD
# ============================================
elif selected_nav == "💰 Salary Estimator":
    st.title("💰 Salary Estimator")
    st.subheader("Estimate your market value based on your skills")
    
    if st.session_state.user_id:
        # Check if user has existing skills
        history = get_user_analyses(st.session_state.user_id)
        all_skills = []
        
        for h in history[:10]:
            try:
                if len(h) > 7 and h[7]:
                    skills_have = json.loads(h[7])
                    if isinstance(skills_have, list):
                        all_skills.extend(skills_have)
            except:
                pass
        
        user_skills = list(set(all_skills))
        
        # Tab layout: Use existing skills or upload new
        tab1, tab2 = st.tabs(["📋 Use My Skills", "📄 Upload Resume"])
        
        with tab1:
            if user_skills:
                st.info(f"🛠️ Your Skills: {', '.join(user_skills[:8])}")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    location = st.selectbox(
                        "📍 Location",
                        ["United States", "United Kingdom", "Canada", "Germany", "Australia", "India", "Uganda", "Kenya", "Nigeria", "South Africa", "Remote"],
                        key="salary_location_skills"
                    )
                
                with col2:
                    experience = st.selectbox(
                        "📊 Experience Level",
                        ["Entry", "Junior", "Mid-Level", "Senior", "Lead", "Principal", "Staff"],
                        key="salary_exp_skills"
                    )
                
                if st.button("💰 Estimate Salary", use_container_width=True, key="salary_estimate_skills"):
                    with st.spinner("Calculating your market value..."):
                        result = estimate_salary(user_skills, experience, location)
                        
                        st.balloons()
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("📊 Average Salary", f"${result['average']:,}")
                        with col2:
                            st.metric("📉 Minimum", f"${result['min']:,}")
                        with col3:
                            st.metric("📈 Maximum", f"${result['max']:,}")
                        
                        st.divider()
                        
                        st.subheader("💰 Salary Breakdown")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown(f"**Base Salary:** ${result['base']:,}")
                            st.markdown(f"**Skills Bonus:** +${result['skill_bonus']:,}")
                        with col2:
                            st.markdown(f"**Experience Bonus:** +${result['experience_bonus']:,}")
                            st.markdown(f"**Location Adjustment:** +${result['location_bonus']:,}")
                        
                        st.divider()
                        st.subheader("📊 Market Comparison")
                        
                        percentile = result.get('percentile', 50)
                        st.progress(percentile/100, text=f"You are in the top {100 - percentile}% of earners")
                        
                        st.caption(f"Market range for {location}: ${result['market_min']:,} - ${result['market_max']:,}")
            else:
                st.info("📄 No skills found. Upload a resume in the 'Upload Resume' tab.")
        
        with tab2:
            st.subheader("📄 Upload a Resume for Salary Estimation")
            
            col1, col2 = st.columns([1, 2])
            with col1:
                uploaded_file = st.file_uploader("Choose a PDF file", type="pdf", key="salary_upload")
            with col2:
                job_title_input = st.text_input("Job Title (Optional)", placeholder="e.g., Software Engineer", key="salary_job_title")
            
            col3, col4 = st.columns(2)
            with col3:
                location = st.selectbox(
                    "📍 Location",
                    ["United States", "United Kingdom", "Canada", "Germany", "Australia", "India", "Uganda", "Kenya", "Nigeria", "South Africa", "Remote"],
                    key="salary_location_upload"
                )
            
            with col4:
                experience = st.selectbox(
                    "📊 Experience Level",
                    ["Entry", "Junior", "Mid-Level", "Senior", "Lead", "Principal", "Staff"],
                    key="salary_exp_upload"
                )
            
            if st.button("💰 Estimate Salary from Resume", use_container_width=True, key="salary_estimate_upload"):
                if uploaded_file:
                    with st.spinner("Analyzing your resume and calculating salary..."):
                        text, err = extract_text(uploaded_file)
                        if err:
                            st.error(f"❌ PDF error: {err}")
                        else:
                            st.success("✅ Resume analyzed successfully!")
                            
                            # Extract skills from resume
                            result = analyze_skills_advanced(text, job_title_input or "Software Engineer")
                            skills_from_resume = result.get("skills_have", [])
                            
                            if skills_from_resume:
                                st.info(f"📋 Skills Found: {', '.join(skills_from_resume)}")
                                
                                # Save the analysis to database
                                if st.session_state.user_id:
                                    analysis_id = save_analysis(st.session_state.user_id, result, text, job_title_input or "Software Engineer")
                                    if analysis_id:
                                        st.success("✅ Results saved to database!")
                                
                                # Calculate salary
                                salary_result = estimate_salary(skills_from_resume, experience, location)
                                
                                st.balloons()
                                
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    st.metric("📊 Average Salary", f"${salary_result['average']:,}")
                                with col2:
                                    st.metric("📉 Minimum", f"${salary_result['min']:,}")
                                with col3:
                                    st.metric("📈 Maximum", f"${salary_result['max']:,}")
                                
                                st.divider()
                                
                                st.subheader("💰 Salary Breakdown")
                                
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.markdown(f"**Base Salary:** ${salary_result['base']:,}")
                                    st.markdown(f"**Skills Bonus:** +${salary_result['skill_bonus']:,}")
                                with col2:
                                    st.markdown(f"**Experience Bonus:** +${salary_result['experience_bonus']:,}")
                                    st.markdown(f"**Location Adjustment:** +${salary_result['location_bonus']:,}")
                                
                                st.divider()
                                st.subheader("📊 Market Comparison")
                                
                                percentile = salary_result.get('percentile', 50)
                                st.progress(percentile/100, text=f"You are in the top {100 - percentile}% of earners")
                                
                                st.caption(f"Market range for {location}: ${salary_result['market_min']:,} - ${salary_result['market_max']:,}")
                            else:
                                st.warning("No skills were extracted from your resume.")
                else:
                    st.error("❌ Please upload a PDF file.")
    else:
        st.warning("🔓 Please login to estimate your salary")

# ============================================
# INTERVIEW QUESTIONS
# ============================================
elif selected_nav == "🎤 Interview Questions":
    st.title("🎤 Interview Questions Generator")
    st.subheader("Prepare for your dream job with custom questions")
    
    if st.session_state.user_id:
        history = get_user_analyses(st.session_state.user_id)
        all_skills = []
        
        for h in history[:10]:
            try:
                if len(h) > 7 and h[7]:
                    skills_have = json.loads(h[7])
                    if isinstance(skills_have, list):
                        all_skills.extend(skills_have)
            except:
                pass
        
        user_skills = list(set(all_skills))
        
        col1, col2 = st.columns(2)
        
        with col1:
            job_title = st.selectbox(
                "💼 Job Title",
                ["Software Engineer", "Data Scientist", "DevOps Engineer", "Frontend Developer", "Backend Developer", "ML Engineer", "Product Manager", "QA Engineer", "Security Engineer"]
            )
        
        with col2:
            experience = st.selectbox(
                "📊 Experience Level",
                ["Entry", "Junior", "Mid-Level", "Senior", "Lead"]
            )
        
        if user_skills:
            st.info(f"🛠️ Your Skills: {', '.join(user_skills[:5])}")
        
        if st.button("🎤 Generate Questions", use_container_width=True):
            with st.spinner("Generating custom interview questions..."):
                questions = generate_questions(job_title, experience, user_skills, num_technical=5, num_behavioral=3)
                
                st.success("✅ Questions generated!")
                st.balloons()
                
                # Technical Questions
                st.subheader("🔹 Technical Questions")
                for i, q in enumerate(questions["technical"], 1):
                    with st.expander(f"Q{i}: {q['question']}"):
                        st.info(f"💡 {q['answer']}")
                
                # Behavioral Questions
                st.subheader("🔹 Behavioral Questions")
                for i, q in enumerate(questions["behavioral"], 1):
                    with st.expander(f"Q{i}: {q['question']}"):
                        st.info(f"💡 {q['answer']}")
                
                # Skill-based Questions
                if questions.get("skill_questions"):
                    st.subheader("🔹 Skill-Based Questions")
                    for i, q in enumerate(questions["skill_questions"], 1):
                        with st.expander(f"Q{i}: {q['question']}"):
                            st.info(f"💡 {q['answer']}")
                
                # Download button
                all_questions_text = ""
                for q in questions["technical"] + questions["behavioral"]:
                    all_questions_text += f"Q: {q['question']}\nAnswer: {q['answer']}\n\n"
                
                st.download_button(
                    label="📥 Download Questions",
                    data=all_questions_text,
                    file_name=f"interview_questions_{job_title.replace(' ', '_')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
    else:
        st.warning("🔓 Please login to generate interview questions")

# ============================================
# FOOTER
# ============================================
st.divider()
st.caption("🚀 SkillBridge - Your AI Career Coach | Made with ❤️ using Python and Streamlit")