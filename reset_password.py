# reset_password.py - Password Reset Functionality

import streamlit as st
import sqlite3
import uuid
import hashlib
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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

def hash_password(password):
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

# ============================================
# EMAIL CONFIGURATION
# ============================================

# For testing without actual email, we'll show the token in the app
# In production, use Gmail SMTP or SendGrid

def send_reset_email(email, reset_token):
    """Send password reset email"""
    try:
        # For testing - just print the token
        reset_link = f"http://localhost:8501?reset_token={reset_token}"
        print(f"📧 Password reset link for {email}: {reset_link}")
        
        # Uncomment this when you have email configured
        # import smtplib
        # from email.mime.text import MIMEText
        # 
        # msg = MIMEText(f"Click here to reset your password: {reset_link}")
        # msg['Subject'] = 'Password Reset - SkillBridge'
        # msg['From'] = 'your_email@gmail.com'
        # msg['To'] = email
        # 
        # server = smtplib.SMTP('smtp.gmail.com', 587)
        # server.starttls()
        # server.login('your_email@gmail.com', 'your_app_password')
        # server.send_message(msg)
        # server.quit()
        
        return True, "Reset link sent to your email"
    except Exception as e:
        return False, str(e)

# ============================================
# PASSWORD RESET FUNCTIONS
# ============================================

def generate_reset_token(email):
    """Generate a password reset token"""
    try:
        token = str(uuid.uuid4())[:8]
        expiry = (datetime.now() + timedelta(hours=1)).isoformat()
        
        conn = get_connection()
        cursor = conn.cursor()
        
        # Add reset token columns if they don't exist (for SQLite)
        try:
            cursor.execute("ALTER TABLE Users ADD COLUMN ResetToken TEXT")
        except:
            pass  # Column already exists
        
        try:
            cursor.execute("ALTER TABLE Users ADD COLUMN ResetTokenExpiry TEXT")
        except:
            pass  # Column already exists
        
        cursor.execute("""
            UPDATE Users 
            SET ResetToken = ?, ResetTokenExpiry = ?
            WHERE Email = ?
        """, (token, expiry, email))
        
        conn.commit()
        conn.close()
        return token
    except Exception as e:
        print(f"❌ Error generating token: {e}")
        return None

def verify_reset_token(token):
    """Verify if reset token is valid"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT Email FROM Users 
            WHERE ResetToken = ? AND ResetTokenExpiry > datetime('now')
        """, (token,))
        
        result = cursor.fetchone()
        conn.close()
        
        return result[0] if result else None
    except Exception as e:
        print(f"❌ Error verifying token: {e}")
        return None

def reset_password(email, new_password):
    """Reset user password"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        hashed = hash_password(new_password)
        
        cursor.execute("""
            UPDATE Users 
            SET PasswordHash = ?, ResetToken = NULL, ResetTokenExpiry = NULL
            WHERE Email = ?
        """, (hashed, email))
        
        conn.commit()
        conn.close()
        return True, "Password reset successful!"
    except Exception as e:
        return False, str(e)

def get_user_by_email(email):
    """Get user by email"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT Email, Name FROM Users WHERE Email = ?", (email,))
        result = cursor.fetchone()
        conn.close()
        return result
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def check_reset_token_exists():
    """Check if there's a reset token in the URL"""
    try:
        # Check if token is in session state or URL
        if "reset_token" in st.session_state:
            return st.session_state.reset_token
        return None
    except:
        return None

# ============================================
# PASSWORD RESET UI
# ============================================

def show_password_reset():
    """Display password reset form"""
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 20px; border-radius: 20px; color: white; text-align: center; margin-bottom: 20px;">
        <h2 style="color: white;">🔒 Reset Password</h2>
        <p style="color: rgba(255,255,255,0.9);">Enter your email to receive a reset link</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Step 1: Enter Email
    email = st.text_input("Email Address", placeholder="your@email.com", key="reset_email")
    
    if st.button("📧 Send Reset Link", use_container_width=True, key="send_reset_btn"):
        if email:
            user = get_user_by_email(email)
            if user:
                token = generate_reset_token(email)
                if token:
                    success, msg = send_reset_email(email, token)
                    if success:
                        st.success(f"✅ {msg}")
                        st.info(f"💡 For testing, your reset token is: `{token}`")
                        st.info("🔗 Use this link: `http://localhost:8501?reset_token=" + token + "`")
                        st.session_state.reset_token = token
                        st.session_state.reset_email = email
                        st.session_state.show_new_password = True
                        st.rerun()
                    else:
                        st.error(f"❌ {msg}")
                else:
                    st.error("❌ Failed to generate reset token")
            else:
                st.error("❌ No account found with this email")
        else:
            st.warning("⚠️ Please enter your email address")
    
    # Step 2: Enter New Password (shown after token is generated)
    if st.session_state.get("show_new_password", False):
        st.divider()
        st.markdown("### 🔑 Set New Password")
        
        new_password = st.text_input("New Password", type="password", placeholder="Enter new password", key="new_pass")
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm new password", key="confirm_pass")
        
        if st.button("✅ Reset Password", use_container_width=True, key="reset_btn"):
            if new_password and confirm_password:
                if new_password == confirm_password:
                    if len(new_password) >= 4:
                        email = st.session_state.get("reset_email")
                        success, msg = reset_password(email, new_password)
                        if success:
                            st.success("✅ Password reset successful! You can now login.")
                            st.session_state.show_new_password = False
                            st.session_state.show_reset = False
                            if st.button("🔙 Go to Login"):
                                st.rerun()
                        else:
                            st.error(f"❌ {msg}")
                    else:
                        st.error("❌ Password must be at least 4 characters")
                else:
                    st.error("❌ Passwords do not match")
            else:
                st.warning("⚠️ Please enter new password")
    
    # Back button
    if st.button("🔙 Back to Login", use_container_width=True):
        st.session_state.show_reset = False
        st.session_state.show_new_password = False
        st.rerun()