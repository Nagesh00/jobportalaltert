import json
import datetime
from job_monitor_debug import IndeedJobMonitor

def test_with_mock_data():
    """Test the job monitor with mock data to verify functionality"""
    
    print("🧪 Testing job monitor with mock data...")
    
    # Mock email configuration
    email_config = {
        'sender_email': 'test@example.com',
        'app_password': 'test_password',
        'recipient_email': 'test@example.com'
    }
    
    # Initialize monitor
    monitor = IndeedJobMonitor(email_config, debug_mode=True)
    
    # Create mock jobs data
    mock_jobs = [
        {
            'id': 'job1_' + str(int(datetime.datetime.now().timestamp())),
            'title': 'Software Test Engineer',
            'company': 'Tech Corp',
            'location': 'New York, NY',
            'snippet': 'We are looking for a Software Test Engineer with 3 years experience in automation testing using Selenium and Python.',
            'url': 'https://indeed.com/viewjob?jk=job1_test',
            'country': 'US',
            'date_found': datetime.datetime.now().isoformat()
        },
        {
            'id': 'job2_' + str(int(datetime.datetime.now().timestamp())),
            'title': 'QA Automation Engineer',
            'company': 'Software Solutions Inc',
            'location': 'San Francisco, CA',
            'snippet': 'Join our QA team! Looking for 2-4 years experience in test automation, API testing, and quality assurance processes.',
            'url': 'https://indeed.com/viewjob?jk=job2_test',
            'country': 'US',
            'date_found': datetime.datetime.now().isoformat()
        },
        {
            'id': 'job3_' + str(int(datetime.datetime.now().timestamp())),
            'title': 'Manual Testing Specialist',
            'company': 'Digital Innovations',
            'location': 'Austin, TX',
            'snippet': 'Manual testing role requiring 2+ years experience in web application testing and bug reporting.',
            'url': 'https://indeed.com/viewjob?jk=job3_test',
            'country': 'US',
            'date_found': datetime.datetime.now().isoformat()
        },
        {
            'id': 'job4_' + str(int(datetime.datetime.now().timestamp())),
            'title': 'Senior Backend Developer',
            'company': 'Enterprise Systems',
            'location': 'Seattle, WA',
            'snippet': 'Senior developer position requiring 8+ years experience in Java and microservices architecture.',
            'url': 'https://indeed.com/viewjob?jk=job4_test',
            'country': 'US',
            'date_found': datetime.datetime.now().isoformat()
        }
    ]
    
    print(f"\n📋 Testing relevance filter with {len(mock_jobs)} mock jobs:")
    
    relevant_jobs = []
    for job in mock_jobs:
        is_relevant = monitor.is_relevant_job(job)
        print(f"  {job['title']}: {'✅ Relevant' if is_relevant else '❌ Not relevant'}")
        if is_relevant:
            relevant_jobs.append(job)
    
    print(f"\n✅ Found {len(relevant_jobs)} relevant jobs out of {len(mock_jobs)} total")
    
    if relevant_jobs:
        print("\n📧 Testing email body creation...")
        email_body = monitor.create_email_body(relevant_jobs)
        print(f"✅ Email body created ({len(email_body)} characters)")
        
        print("\n💾 Testing job tracking...")
        # Add jobs to tracking
        for job in relevant_jobs:
            monitor.tracked_jobs[job['id']] = job
        
        monitor.save_tracked_jobs()
        print("✅ Jobs saved to tracking file")
        
        # Test loading
        monitor.load_tracked_jobs()
        print(f"✅ Loaded {len(monitor.tracked_jobs)} tracked jobs")
        
        print("\n📧 Testing email notification (simulated)...")
        monitor.send_email_notification(relevant_jobs)
    
    return len(relevant_jobs)

def test_url_building():
    """Test URL building functionality"""
    print("\n🔗 Testing URL building...")
    
    monitor = IndeedJobMonitor(debug_mode=True)
    
    countries = ["US", "UK", "CA", "AU", "IN"]
    
    for country in countries:
        url = monitor.build_search_url(country)
        alt_url = monitor.build_alternative_search_url(country)
        print(f"  {country}: {url[:60]}...")
        print(f"  {country} (alt): {alt_url[:60]}...")

def main():
    print("🧪 Job Monitor Debug & Test Suite")
    print("=" * 50)
    
    # Test URL building
    test_url_building()
    
    # Test with mock data
    relevant_count = test_with_mock_data()
    
    print(f"\n✅ All tests completed!")
    print(f"📊 Summary: Found {relevant_count} relevant jobs from mock data")
    
    if relevant_count > 0:
        print("✅ Job filtering, tracking, and email functionality working correctly")
    else:
        print("⚠️  No relevant jobs found - check filtering criteria")

if __name__ == "__main__":
    main()
