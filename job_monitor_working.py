# Job Monitor - Alternative Approaches
# This file contains alternative job monitoring methods that are more reliable than web scraping

import requests
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
import time
import os
from urllib.parse import quote
import feedparser
import random

class AlternativeJobMonitor:
    def __init__(self, email_config):
        self.email_config = email_config
        self.jobs_file = "tracked_jobs_alt.json"
        self.load_tracked_jobs()
        
    def load_tracked_jobs(self):
        """Load previously tracked jobs from file"""
        try:
            with open(self.jobs_file, 'r') as f:
                self.tracked_jobs = json.load(f)
        except FileNotFoundError:
            self.tracked_jobs = {}
    
    def save_tracked_jobs(self):
        """Save tracked jobs to file"""
        with open(self.jobs_file, 'w') as f:
            json.dump(self.tracked_jobs, f, indent=2)
    
    def search_github_jobs(self):
        """Search GitHub Jobs API (if still available)"""
        jobs = []
        try:
            print("🔍 Searching GitHub Jobs...")
            
            # GitHub Jobs was discontinued, but we can simulate the structure
            # In practice, you'd replace this with other job APIs
            
            # Placeholder for demonstration
            print("ℹ️  GitHub Jobs API has been discontinued")
            
        except Exception as e:
            print(f"❌ Error accessing GitHub Jobs: {str(e)}")
        
        return jobs
    
    def search_remoteok_api(self):
        """Search RemoteOK API"""
        jobs = []
        try:
            print("🔍 Searching RemoteOK...")
            
            url = "https://remoteok.io/api"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                
                # Filter for testing jobs
                for job in data[1:]:  # Skip the first item (metadata)
                    if self.is_testing_job(job.get('position', ''), job.get('description', '')):
                        job_data = {
                            'id': f"remoteok_{job.get('id', '')}",
                            'title': job.get('position', 'N/A'),
                            'company': job.get('company', 'N/A'),
                            'location': 'Remote',
                            'snippet': job.get('description', 'N/A')[:300],
                            'url': f"https://remoteok.io/remote-jobs/{job.get('id', '')}",
                            'country': 'Remote',
                            'date_found': datetime.datetime.now().isoformat(),
                            'source': 'RemoteOK'
                        }
                        jobs.append(job_data)
                
                print(f"✅ Found {len(jobs)} testing jobs on RemoteOK")
                
        except Exception as e:
            print(f"❌ Error accessing RemoteOK: {str(e)}")
        
        return jobs
    
    def search_jobs_rss_feeds(self):
        """Search job RSS feeds"""
        jobs = []
        
        # List of RSS feeds to check
        rss_feeds = [
            {
                'name': 'Stack Overflow Jobs',
                'url': 'https://stackoverflow.com/jobs/feed?q=software+testing',
                'disabled': True  # Stack Overflow Jobs was discontinued
            }
            # Add more RSS feeds here as available
        ]
        
        for feed_info in rss_feeds:
            if feed_info.get('disabled'):
                print(f"ℹ️  {feed_info['name']} is no longer available")
                continue
                
            try:
                print(f"🔍 Checking {feed_info['name']} RSS feed...")
                
                feed = feedparser.parse(feed_info['url'])
                
                for entry in feed.entries[:20]:  # Limit to recent entries
                    if self.is_testing_job(entry.title, getattr(entry, 'summary', '')):
                        job_data = {
                            'id': f"rss_{hash(entry.link)}",
                            'title': entry.title,
                            'company': 'Various',
                            'location': 'Various',
                            'snippet': getattr(entry, 'summary', 'N/A')[:300],
                            'url': entry.link,
                            'country': 'Various',
                            'date_found': datetime.datetime.now().isoformat(),
                            'source': feed_info['name']
                        }
                        jobs.append(job_data)
                
                print(f"✅ Found {len(jobs)} jobs from {feed_info['name']}")
                
            except Exception as e:
                print(f"❌ Error accessing {feed_info['name']}: {str(e)}")
        
        return jobs
    
    def create_sample_jobs(self):
        """Create sample jobs for demonstration purposes"""
        print("🧪 Creating sample jobs for demonstration...")
        
        sample_jobs = [
            {
                'id': f'demo_qa_engineer_{int(datetime.datetime.now().timestamp())}',
                'title': 'QA Automation Engineer',
                'company': 'TechCorp Solutions',
                'location': 'New York, NY (Remote)',
                'snippet': 'We are seeking a QA Automation Engineer with 3-5 years of experience in test automation frameworks like Selenium, Cypress, and API testing. Must have experience with CI/CD pipelines and Agile methodologies.',
                'url': 'https://example.com/jobs/qa-engineer',
                'country': 'US',
                'date_found': datetime.datetime.now().isoformat(),
                'source': 'Demo'
            },
            {
                'id': f'demo_sdet_{int(datetime.datetime.now().timestamp())}',
                'title': 'Software Development Engineer in Test (SDET)',
                'company': 'Innovation Labs',
                'location': 'San Francisco, CA',
                'snippet': 'Join our growing team as an SDET! We need someone with 2-4 years experience in automated testing, Python/Java programming, and experience with testing frameworks. Knowledge of Docker and Kubernetes is a plus.',
                'url': 'https://example.com/jobs/sdet',
                'country': 'US',
                'date_found': datetime.datetime.now().isoformat(),
                'source': 'Demo'
            },
            {
                'id': f'demo_manual_tester_{int(datetime.datetime.now().timestamp())}',
                'title': 'Manual QA Tester',
                'company': 'StartupXYZ',
                'location': 'Austin, TX',
                'snippet': 'Looking for a detail-oriented Manual QA Tester with 2+ years of experience in web application testing, mobile testing, and bug reporting. Experience with test case design and execution required.',
                'url': 'https://example.com/jobs/manual-tester',
                'country': 'US',
                'date_found': datetime.datetime.now().isoformat(),
                'source': 'Demo'
            }
        ]
        
        # Filter out jobs we've already seen
        new_jobs = []
        for job in sample_jobs:
            if job['id'] not in self.tracked_jobs:
                new_jobs.append(job)
        
        print(f"✅ Created {len(new_jobs)} new demo jobs")
        return new_jobs
    
    def is_testing_job(self, title, description):
        """Check if a job is related to software testing"""
        title_lower = title.lower()
        desc_lower = description.lower()
        
        testing_keywords = [
            'test', 'testing', 'qa', 'quality assurance', 'automation',
            'selenium', 'cypress', 'junit', 'pytest', 'tester', 'sdet'
        ]
        
        return any(keyword in title_lower or keyword in desc_lower 
                  for keyword in testing_keywords)
    
    def send_email_notification(self, new_jobs):
        """Send email notification for new jobs"""
        if not new_jobs:
            return
        
        if not self.email_config or not all(self.email_config.values()):
            print(f"📧 Would send email notification for {len(new_jobs)} jobs (email config missing)")
            self.print_jobs_summary(new_jobs)
            return
            
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_config['sender_email']
            msg['To'] = self.email_config['recipient_email']
            msg['Subject'] = f"🎯 {len(new_jobs)} New Software Testing Jobs Found!"
            
            # Create email body
            body = self.create_email_body(new_jobs)
            msg.attach(MIMEText(body, 'html'))
            
            # Send email
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.email_config['sender_email'], self.email_config['app_password'])
            
            text = msg.as_string()
            server.sendmail(self.email_config['sender_email'], self.email_config['recipient_email'], text)
            server.quit()
            
            print(f"📧 Email sent successfully with {len(new_jobs)} jobs!")
            
        except Exception as e:
            print(f"❌ Error sending email: {str(e)}")
            # Show jobs in console as fallback
            self.print_jobs_summary(new_jobs)
    
    def print_jobs_summary(self, jobs):
        """Print jobs summary to console"""
        print(f"\n📋 Jobs Summary ({len(jobs)} jobs):")
        print("=" * 60)
        
        for i, job in enumerate(jobs, 1):
            print(f"\n{i}. {job['title']}")
            print(f"   🏢 Company: {job['company']}")
            print(f"   📍 Location: {job['location']}")
            print(f"   🌐 Source: {job.get('source', 'Unknown')}")
            print(f"   📝 Description: {job['snippet'][:100]}...")
            print(f"   🔗 URL: {job['url']}")
    
    def create_email_body(self, jobs):
        """Create HTML email body"""
        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .job {{ border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px; }}
                .job-title {{ color: #2557a7; font-weight: bold; font-size: 18px; }}
                .company {{ color: #666; font-size: 16px; margin: 5px 0; }}
                .location {{ color: #888; font-size: 14px; }}
                .snippet {{ margin: 10px 0; font-size: 14px; }}
                .source {{ color: #999; font-size: 12px; font-style: italic; }}
                .apply-btn {{ background-color: #2557a7; color: white; padding: 10px 20px; 
                           text-decoration: none; border-radius: 5px; display: inline-block; margin-top: 10px; }}
            </style>
        </head>
        <body>
            <h2>🎯 New Software Testing Jobs</h2>
            <p>Found {len(jobs)} new jobs matching your criteria:</p>
        """
        
        for job in jobs:
            html += f"""
            <div class="job">
                <div class="job-title">{job['title']}</div>
                <div class="company">🏢 {job['company']}</div>
                <div class="location">📍 {job['location']}</div>
                <div class="source">📊 Source: {job.get('source', 'Unknown')}</div>
                <div class="snippet">{job['snippet'][:200]}...</div>
                <a href="{job['url']}" class="apply-btn">View Job</a>
            </div>
            """
        
        html += """
        </body>
        </html>
        """
        
        return html
    
    def run_monitoring(self):
        """Main monitoring function using alternative methods"""
        print("🔍 Starting alternative job monitoring...")
        
        all_new_jobs = []
        
        # Try different sources
        sources = [
            self.search_remoteok_api,
            self.search_jobs_rss_feeds,
            self.create_sample_jobs  # For demonstration
        ]
        
        for source_func in sources:
            try:
                jobs = source_func()
                for job in jobs:
                    if job['id'] not in self.tracked_jobs:
                        self.tracked_jobs[job['id']] = job
                        all_new_jobs.append(job)
            except Exception as e:
                print(f"❌ Error with job source: {str(e)}")
        
        if all_new_jobs:
            print(f"✅ Found {len(all_new_jobs)} new jobs!")
            self.send_email_notification(all_new_jobs)
            self.save_tracked_jobs()
        else:
            print("ℹ️ No new jobs found.")
        
        return len(all_new_jobs)

def main():
    print("🤖 Alternative Job Monitor")
    print("Uses multiple sources instead of web scraping Indeed")
    print("=" * 60)
    
    # Email configuration
    email_config = {
        'sender_email': os.environ.get('SENDER_EMAIL'),
        'app_password': os.environ.get('EMAIL_APP_PASSWORD'),
        'recipient_email': os.environ.get('RECIPIENT_EMAIL')
    }
    
    # Initialize and run monitor
    monitor = AlternativeJobMonitor(email_config)
    new_jobs_count = monitor.run_monitoring()
    
    print(f"\n✅ Job monitoring completed. Found {new_jobs_count} new jobs.")
    
    print(f"\n💡 Tips for production use:")
    print("1. Replace demo jobs with real API integrations")
    print("2. Add more job board APIs (AngelList, LinkedIn, etc.)")
    print("3. Use official RSS feeds where available")
    print("4. Consider paid job aggregation services")
    print("5. Set up proper email credentials for notifications")

if __name__ == "__main__":
    main()
