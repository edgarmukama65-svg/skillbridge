# email_service.py - Email Service for SkillBridge

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email_config import *

# ============================================
# EMAIL TEMPLATES
# ============================================

def get_welcome_template(name):
    """Generate welcome email HTML template"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; background-color: #f5f7fa; padding: 20px; }}
            .container {{ max-width: 600px; margin: 0 auto; background: white; border-radius: 20px; padding: 40px; box-shadow: 0 10px 40px rgba(0,0,0,0.1); }}
            .header {{ text-align: center; padding-bottom: 20px; border-bottom: 2px solid #667eea; }}
            .logo {{ font-size: 48px; }}
            .title {{ font-size: 28px; color: #1a1a2e; }}
            .subtitle {{ color: #666; font-size: 16px; }}
            .content {{ padding: 20px 0; }}
            .feature {{ background: #f8f9ff; padding: 15px; border-radius: 10px; margin: 10px 0; border-left: 4px solid #667eea; }}
            .footer {{ text-align: center; color: #999; font-size: 12px; padding-top: 20px; border-top: 1px solid #eee; }}
            .button {{ background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 12px 30px; border-radius: 30px; text-decoration: none; display: inline-block; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="logo">🚀</div>
                <h1 class="title">Welcome to SkillBridge!</h1>
                <p class="subtitle">Your AI Career Coach</p>
            </div>
            
            <div class="content">
                <p>Hi <strong>{name}</strong>! 👋</p>
                <p>We're excited to help you advance your career with SkillBridge!</p>
                
                <div class="feature">
                    <strong>📄 Upload Your Resume</strong>
                    <p style="margin: 5px 0 0 0; color: #666;">Get instant feedback on your resume's ATS score</p>
                </div>
                
                <div class="feature">
                    <strong>🔍 Discover Skill Gaps</strong>
                    <p style="margin: 5px 0 0 0; color: #666;">Find out what skills you need to land your dream job</p>
                </div>
                
                <div class="feature">
                    <strong>📚 Personalized Learning Roadmap</strong>
                    <p style="margin: 5px 0 0 0; color: #666;">Get a step-by-step plan to acquire the right skills</p>
                </div>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="https://skillbridge-9jb7lyqdqen92empuxkjkk.streamlit.app" class="button">Get Started Now</a>
                </div>
                
                <p>We're here to help you succeed! If you have any questions, feel free to reply to this email.</p>
                
                <p>Best regards,<br>The SkillBridge Team 🚀</p>
            </div>
            
            <div class="footer">
                <p>© 2026 SkillBridge. All rights reserved.</p>
                <p>You received this email because you registered on SkillBridge.</p>
            </div>
        </div>
    </body>
    </html>
    """

def get_password_reset_template(name, reset_link):
    """Generate password reset email HTML template"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; background-color: #f5f7fa; padding: 20px; }}
            .container {{ max-width: 600px; margin: 0 auto; background: white; border-radius: 20px; padding: 40px; box-shadow: 0 10px 40px rgba(0,0,0,0.1); }}
            .header {{ text-align: center; padding-bottom: 20px; border-bottom: 2px solid #f5576c; }}
            .logo {{ font-size: 48px; }}
            .title {{ font-size: 28px; color: #1a1a2e; }}
            .content {{ padding: 20px 0; }}
            .warning {{ background: #fff5f5; padding: 15px; border-radius: 10px; margin: 10px 0; border-left: 4px solid #f5576c; }}
            .footer {{ text-align: center; color: #999; font-size: 12px; padding-top: 20px; border-top: 1px solid #eee; }}
            .button {{ background: linear-gradient(135deg, #f5576c, #f093fb); color: white; padding: 12px 30px; border-radius: 30px; text-decoration: none; display: inline-block; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="logo">🔒</div>
                <h1 class="title">Password Reset</h1>
            </div>
            
            <div class="content">
                <p>Hi <strong>{name}</strong>,</p>
                <p>We received a request to reset your password for your SkillBridge account.</p>
                
                <div class="warning">
                    <strong>⚠️ Did you request this?</strong>
                    <p style="margin: 5px 0 0 0; color: #666;">If you didn't request a password reset, please ignore this email.</p>
                </div>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{reset_link}" class="button">Reset Password</a>
                </div>
                
                <p>This link will expire in <strong>1 hour</strong>.</p>
                
                <p>If you're having trouble clicking the button, copy and paste this link into your browser:</p>
                <p style="color: #667eea; font-size: 12px; word-break: break-all;">{reset_link}</p>
                
                <p>Best regards,<br>The SkillBridge Team 🚀</p>
            </div>
            
            <div class="footer">
                <p>© 2026 SkillBridge. All rights reserved.</p>
                <p>You received this email because you requested a password reset.</p>
            </div>
        </div>
    </body>
    </html>
    """

# ============================================
# EMAIL SENDING FUNCTIONS
# ============================================

def send_email(to_email, subject, html_content):
    """
    Send email using SMTP
    Returns: True if sent successfully, False otherwise
    """
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(html_content, 'html'))
        
        print(f"📧 Sending email to {to_email}...")
        
        # Connect to SMTP server
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        print(f"✅ Email sent to {to_email}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send email: {str(e)}")
        return False

def send_welcome_email(name, email):
    """Send welcome email to new user"""
    html_content = get_welcome_template(name)
    return send_email(email, WELCOME_SUBJECT, html_content)

def send_password_reset_email(name, email, reset_link):
    """Send password reset email"""
    html_content = get_password_reset_template(name, reset_link)
    return send_email(email, PASSWORD_RESET_SUBJECT, html_content)

# ============================================
# TEST FUNCTION
# ============================================

def test_email():
    """Test email sending"""
    print("📧 Testing email service...")
    
    # Test welcome email
    success = send_welcome_email("Test User", "test@example.com")
    if success:
        print("✅ Welcome email test passed!")
    else:
        print("❌ Welcome email test failed")
    
    # Test password reset email
    success = send_password_reset_email(
        "Test User", 
        "test@example.com", 
        "http://localhost:8501?reset_token=test123"
    )
    if success:
        print("✅ Password reset email test passed!")
    else:
        print("❌ Password reset email test failed")

if __name__ == "__main__":
    test_email()