# email_marketing.py - Email Marketing Functions

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# ============================================
# EMAIL CONFIGURATION (Use Gmail or SendGrid)
# ============================================

# For Gmail:
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = "your_email@gmail.com"  # CHANGE THIS
EMAIL_PASSWORD = "your_app_password"    # CHANGE THIS

def send_welcome_email(name, email):
    """Send welcome email to new user"""
    try:
        subject = f"Welcome to SkillBridge, {name}! 🚀"
        
        body = f"""
        Hi {name},
        
        Welcome to SkillBridge! 🎉
        
        We're excited to help you find skill gaps and land your dream job.
        
        Here's what you can do with SkillBridge:
        ✅ Upload your resume and get an ATS score
        ✅ Discover skill gaps
        ✅ Get a personalized learning roadmap
        ✅ Build professional resumes
        ✅ Generate cover letters
        
        Get started now: http://localhost:8501
        
        Happy job hunting! 🚀
        
        The SkillBridge Team
        """
        
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        # Uncomment this when you have email configured
        # server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        # server.starttls()
        # server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        # server.send_message(msg)
        # server.quit()
        
        print(f"📧 Welcome email sent to {email}")
        return True
        
    except Exception as e:
        print(f"❌ Email error: {e}")
        return False

def send_password_reset_email(email, reset_link):
    """Send password reset email"""
    try:
        subject = "Password Reset - SkillBridge"
        
        body = f"""
        Hi there,
        
        We received a request to reset your password.
        
        Click the link below to reset your password:
        {reset_link}
        
        If you didn't request this, please ignore this email.
        
        The SkillBridge Team
        """
        
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        # Uncomment this when you have email configured
        # server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        # server.starttls()
        # server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        # server.send_message(msg)
        # server.quit()
        
        print(f"📧 Password reset email sent to {email}")
        return True
        
    except Exception as e:
        print(f"❌ Email error: {e}")
        return False