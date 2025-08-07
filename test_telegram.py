import os
import sys
import datetime

# Add current directory to path to import job_monitor
sys.path.append('.')

from job_monitor import IndeedJobMonitor

def test_telegram_notification():
    """Test Telegram notification with your credentials"""
    
    print("🧪 Testing Telegram Notification")
    print("=" * 40)
    
    # Your Telegram configuration
    telegram_config = {
        'bot_token': '8305949318:AAF257TSUv4EObGWLAAi7Cq7K87iambC9EM',
        'chat_id': '6411380646'
    }
    
    # Mock email config (not used for this test)
    email_config = {
        'sender_email': None,
        'app_password': None,
        'recipient_email': None
    }
    
    # Initialize monitor
    monitor = IndeedJobMonitor(email_config, telegram_config)
    
    # Create test jobs
    test_jobs = [
        {
            'id': f'test_job_1_{int(datetime.datetime.now().timestamp())}',
            'title': 'QA Automation Engineer',
            'company': 'TechCorp Solutions',
            'location': 'New York, NY (Remote)',
            'snippet': 'We are seeking a QA Automation Engineer with 3-5 years of experience in test automation frameworks like Selenium, Cypress, and API testing.',
            'url': 'https://example.com/jobs/qa-engineer',
            'country': 'US',
            'date_found': datetime.datetime.now().isoformat()
        },
        {
            'id': f'test_job_2_{int(datetime.datetime.now().timestamp())}',
            'title': 'Software Test Engineer',
            'company': 'Innovation Labs',
            'location': 'San Francisco, CA',
            'snippet': 'Join our testing team! Looking for 2-4 years experience in manual and automated testing, bug reporting, and quality assurance processes.',
            'url': 'https://example.com/jobs/test-engineer',
            'country': 'US',
            'date_found': datetime.datetime.now().isoformat()
        }
    ]
    
    print(f"📱 Sending test notification with {len(test_jobs)} jobs to Telegram...")
    
    # Test Telegram notification
    monitor.send_telegram_notification(test_jobs)
    
    print("✅ Test completed! Check your Telegram for the notification.")

if __name__ == "__main__":
    test_telegram_notification()
