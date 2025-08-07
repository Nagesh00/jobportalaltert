#!/usr/bin/env python3
"""
Email Test Script for Job Monitor
Tests email configuration with your credentials
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def test_email_configuration():
    """Test email sending with your configuration"""
    
    # Your email configuration
    sender_email = "kalyogyogi@gmail.com"
    recipient_email = "kalyogyogi@gmail.com"  # Sending to yourself for testing
    app_password = os.environ.get('EMAIL_APP_PASSWORD')
    
    if not app_password:
        print("❌ EMAIL_APP_PASSWORD environment variable not set!")
        print("Please set it with your Gmail App Password")
        print("Run: $env:EMAIL_APP_PASSWORD='your-app-password'")
        return False
    
    print(f"📧 Testing email configuration...")
    print(f"From: {sender_email}")
    print(f"To: {recipient_email}")
    
    try:
        # Create test email
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = "🧪 Job Monitor Email Test - Working!"
        
        # Email body
        body = """
        <html>
        <head></head>
        <body>
            <h2>✅ Job Monitor Email Test Successful!</h2>
            <p>This is a test email from your job monitoring bot.</p>
            <p><strong>Configuration Details:</strong></p>
            <ul>
                <li>Sender: kalyogyogi@gmail.com</li>
                <li>Recipient: kalyogyogi@gmail.com</li>
                <li>SMTP: Gmail</li>
            </ul>
            <p>If you received this email, your email notifications are working correctly!</p>
            <p>🎯 Your job monitor will now send real job alerts to this email address.</p>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(body, 'html'))
        
        # Connect to Gmail SMTP
        print("🔐 Connecting to Gmail SMTP...")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        
        print("🔑 Authenticating...")
        server.login(sender_email, app_password)
        
        print("📤 Sending test email...")
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        
        print("✅ Test email sent successfully!")
        print("📬 Check your inbox at kalyogyogi@gmail.com")
        return True
        
    except smtplib.SMTPAuthenticationError:
        print("❌ SMTP Authentication failed!")
        print("Please check:")
        print("1. Your Gmail App Password is correct")
        print("2. 2-Factor Authentication is enabled on your Gmail")
        print("3. App Password is generated from Google Account settings")
        return False
        
    except Exception as e:
        print(f"❌ Error sending email: {str(e)}")
        return False

def main():
    print("🧪 Job Monitor Email Test")
    print("=" * 50)
    
    success = test_email_configuration()
    
    if success:
        print("\n🎉 Email configuration is working!")
        print("Your job monitor will now send email notifications.")
    else:
        print("\n💡 To fix email issues:")
        print("1. Enable 2-Factor Authentication on your Gmail")
        print("2. Generate an App Password: https://myaccount.google.com/apppasswords")
        print("3. Set the environment variable:")
        print("   $env:EMAIL_APP_PASSWORD='your-16-character-app-password'")

if __name__ == "__main__":
    main()
