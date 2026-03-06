"""
Email Utility - Sends emails for OTP and password reset.

In production, integrate with SendGrid, AWS SES, or similar.
For demo, logs emails to console.
"""

import os
from typing import Optional


def send_otp_email(email: str, otp_code: str, username: str = "User") -> bool:
    """
    Send OTP via email.
    
    Args:
        email: Recipient email address
        otp_code: 6-digit OTP code
        username: User's name for personalization
        
    Returns:
        True if email sent successfully, False otherwise
    """
    subject = "Your Password Reset OTP"
    body = f"""
Hello {username},

You requested to reset your password. Your One-Time Password (OTP) is:

    {otp_code}

This OTP is valid for 10 minutes only.

If you did not request this, please ignore this email.

Best regards,
Financial Monitoring System Team
"""
    
    return _send_email(email, subject, body)


def send_password_reset_link_email(
    email: str, 
    reset_token: str, 
    username: str = "User",
    app_url: str = "http://localhost:5173"
) -> bool:
    """
    Send password reset link via email.
    
    Args:
        email: Recipient email address
        reset_token: JWT password reset token
        username: User's name for personalization
        app_url: Frontend URL for reset link
        
    Returns:
        True if email sent successfully, False otherwise
    """
    reset_link = f"{app_url}/reset-password?token={reset_token}"
    subject = "Password Reset Request"
    body = f"""
Hello {username},

Click the link below to reset your password:

    {reset_link}

This link is valid for 1 hour only.

If you did not request this, please ignore this email.

Best regards,
Financial Monitoring System Team
"""
    
    return _send_email(email, subject, body)


def send_welcome_email(email: str, username: str) -> bool:
    """
    Send welcome email to new user.
    
    Args:
        email: Recipient email address
        username: User's name
        
    Returns:
        True if email sent successfully, False otherwise
    """
    subject = "Welcome to Financial Monitoring System"
    body = f"""
Hello {username},

Welcome to the Financial Monitoring System!

Your account has been created successfully. You can now log in and start managing your portfolio.

If you have any questions, feel free to reach out to our support team.

Best regards,
Financial Monitoring System Team
"""
    
    return _send_email(email, subject, body)


def _send_email(to_email: str, subject: str, body: str) -> bool:
    """
    Internal email sending function.
    
    In production, this would integrate with:
    - SendGrid API
    - AWS SES
    - Mailgun
    - SMTP server
    
    For now, logs to console.
    
    Args:
        to_email: Recipient email
        subject: Email subject
        body: Email body
        
    Returns:
        True if email sent (or logged), False on error
    """
    try:
        # Check if we have email configuration
        smtp_server = os.getenv("SMTP_SERVER")
        smtp_port = os.getenv("SMTP_PORT")
        sender_email = os.getenv("SENDER_EMAIL")
        sender_password = os.getenv("SENDER_PASSWORD")
        
        if smtp_server and sender_email:
            # Try to send via SMTP
            _send_via_smtp(to_email, subject, body, smtp_server, int(smtp_port or 587), sender_email, sender_password)
            print(f"[Email] Email sent to {to_email}")
            return True
        else:
            # Demo mode - just log it
            print(f"\n{'='*60}")
            print(f"[EMAIL SERVICE - DEMO MODE]")
            print(f"To: {to_email}")
            print(f"Subject: {subject}")
            print(f"{body}")
            print(f"{'='*60}\n")
            return True
            
    except Exception as e:
        print(f"[Email] Failed to send email to {to_email}: {e}")
        return False


def _send_via_smtp(to_email: str, subject: str, body: str, smtp_server: str, 
                   smtp_port: int, sender_email: str, sender_password: str) -> None:
    """
    Send email via SMTP (requires email configuration in environment).
    
    Args:
        to_email: Recipient email
        subject: Email subject
        body: Email body
        smtp_server: SMTP server address
        smtp_port: SMTP port
        sender_email: Sender email address
        sender_password: Sender email password or API key
    """
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    
    try:
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = to_email
        msg["Subject"] = subject
        
        msg.attach(MIMEText(body, "plain"))
        
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            
    except Exception as e:
        raise Exception(f"SMTP Error: {e}")
