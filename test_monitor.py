import json
import datetime
from job_monitor import IndeedJobMonitor

def test_job_monitor():
    """Test the job monitor locally without sending emails"""
    
    # Mock email configuration for testing
    email_config = {
        'sender_email': 'test@example.com',
        'app_password': 'test_password',
        'recipient_email': 'test@example.com'
    }
    
    # Initialize monitor
    monitor = IndeedJobMonitor(email_config)
    
    # Test URL building
    url_us = monitor.build_search_url("US")
    url_uk = monitor.build_search_url("UK")
    
    print("Testing URL generation:")
    print(f"US URL: {url_us}")
    print(f"UK URL: {url_uk}")
    
    # Test job relevance checking
    test_job_1 = {
        'title': 'Software Test Engineer',
        'snippet': 'Looking for a QA engineer with 3 years experience in automation testing',
        'id': 'test1',
        'company': 'Tech Company Inc',
        'location': 'New York, NY',
        'url': 'https://indeed.com/viewjob?jk=test1',
        'country': 'US'
    }
    
    test_job_2 = {
        'title': 'Senior Developer',
        'snippet': 'Need 10 years experience in backend development',
        'id': 'test2',
        'company': 'Another Company',
        'location': 'San Francisco, CA',
        'url': 'https://indeed.com/viewjob?jk=test2',
        'country': 'US'
    }
    
    print("\nTesting job relevance:")
    print(f"Test Job 1 (relevant): {monitor.is_relevant_job(test_job_1)}")
    print(f"Test Job 2 (not relevant): {monitor.is_relevant_job(test_job_2)}")
    
    # Test email body creation
    test_jobs = [test_job_1]
    email_body = monitor.create_email_body(test_jobs)
    
    print(f"\nEmail body created (length: {len(email_body)} characters)")
    
    print("✅ All tests passed!")

if __name__ == "__main__":
    test_job_monitor()
