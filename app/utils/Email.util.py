
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()


class EmailUtil:
    """Utility class for sending emails"""
    
    # Email configuration
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', 'your-email@gmail.com')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', 'your-app-password')
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
    
    
    @staticmethod #Basically sends user email
    def send_otp_email(to_email, otp, user_name=None):
       
        try:
            # Email subject
            subject = "Your OTP for Password Reset"
            
            # Email body
            if user_name:
                body = f"""
                <html>
                    <body>
                        <h2>Hello {user_name},</h2>
                        
                        <p>You requested a password reset for your Financial Dashboard account.</p>
                        
                        <p>Your One-Time Password (OTP) is:</p>
                        <h1 style="color: blue; font-size: 30px;">{otp}</h1>
                        
                        <p><strong>Note:</strong> This OTP is valid for 10 minutes only.</p>
                        
                        <p>If you didn't request this, please ignore this email.</p>
                        
                        <br>
                        <p>Best regards,<br>Financial Dashboard Team</p>
                    </body>
                </html>
                """
            else:
                body = f"""
                <html>
                    <body>
                        <h2>Password Reset OTP</h2>
                        
                        <p>Your One-Time Password (OTP) is:</p>
                        <h1 style="color: blue; font-size: 30px;">{otp}</h1>
                        
                        <p>This OTP is valid for 10 minutes.</p>
                    </body>
                </html>
                """
            
            # Send email
            EmailUtil._send_email(to_email, subject, body)
            print(f"✅ OTP email sent to {to_email}")
            return True
        
        except Exception as e:
            print(f"❌ Failed to send OTP email: {e}")
            return False
    
    
    @staticmethod
    def send_password_reset_email(to_email, reset_link, user_name=None):
   
        try:
            subject = "Reset Your Password"
            
            if user_name:
                body = f"""
                <html>
                    <body>
                        <h2>Hello {user_name},</h2>
                        
                        <p>Click the link below to reset your password:</p>
                        
                        <p><a href="{reset_link}" style="background-color: blue; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Reset Password</a></p>
                        
                        <p>Or copy and paste this link:</p>
                        <p>{reset_link}</p>
                        
                        <p><strong>Note:</strong> This link is valid for 1 hour only.</p>
                        
                        <p>If you didn't request this, please ignore this email.</p>
                        
                        <br>
                        <p>Best regards,<br>Financial Dashboard Team</p>
                    </body>
                </html>
                """
            else:
                body = f"""
                <html>
                    <body>
                        <h2>Reset Your Password</h2>
                        <p>Click here to reset: <a href="{reset_link}">{reset_link}</a></p>
                    </body>
                </html>
                """
            
            EmailUtil._send_email(to_email, subject, body)
            print(f"✅ Password reset email sent to {to_email}")
            return True
        
        except Exception as e:
            print(f"❌ Failed to send password reset email: {e}")
            return False
    
    
    @staticmethod
    def send_verification_email(to_email, verification_link, user_name=None):
    
        try:
            subject = "Verify Your Email Address"
            
            if user_name:
                body = f"""
                <html>
                    <body>
                        <h2>Hello {user_name},</h2>
                        
                        <p>Welcome to Financial Dashboard!</p>
                        
                        <p>Click the link below to verify your email:</p>
                        
                        <p><a href="{verification_link}" style="background-color: green; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Verify Email</a></p>
                        
                        <p>Or copy and paste this link:</p>
                        <p>{verification_link}</p>
                        
                        <br>
                        <p>Best regards,<br>Financial Dashboard Team</p>
                    </body>
                </html>
                """
            else:
                body = f"""
                <html>
                    <body>
                        <h2>Verify Your Email</h2>
                        <p>Click here to verify: <a href="{verification_link}">{verification_link}</a></p>
                    </body>
                </html>
                """
            
            EmailUtil._send_email(to_email, subject, body)
            print(f"✅ Verification email sent to {to_email}")
            return True
        
        except Exception as e:
            print(f"❌ Failed to send verification email: {e}")
            return False
    
    
    @staticmethod
    def _send_email(to_email, subject, body):
     
        # Create email message
        message = MIMEMultipart('alternative')
        message['From'] = EmailUtil.MAIL_USERNAME
        message['To'] = to_email
        message['Subject'] = subject
        
        # Attach HTML body
        message.attach(MIMEText(body, 'html'))
        
        # Connect to SMTP server and send
        try:
            server = smtplib.SMTP(EmailUtil.MAIL_SERVER, EmailUtil.MAIL_PORT)
            
            if EmailUtil.MAIL_USE_TLS:
                server.starttls()
            
            server.login(EmailUtil.MAIL_USERNAME, EmailUtil.MAIL_PASSWORD)
            server.send_message(message)
            server.quit()
            
            print(f"✅ Email sent to {to_email}")
        
        except Exception as e:
            print(f"❌ SMTP Error: {e}")
            raise