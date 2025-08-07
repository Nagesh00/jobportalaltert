#!/usr/bin/env python3
"""
ENHANCED REAL-TIME Job Monitor with Multiple Sources
Provides immediate alerts for real testing jobs from multiple sources
"""

import requests
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
import time
import os
import threading
from concurrent.futures import ThreadPoolExecutor
import feedparser

class EnhancedRealTimeMonitor:
    def __init__(self, email_config, telegram_config):
        self.email_config = email_config
        self.telegram_config = telegram_config
        self.jobs_file = "enhanced_realtime_jobs.json"
        self.load_tracked_jobs()
        self.scan_count = 0
        
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
    
    def check_remoteok_enhanced(self):
        """Enhanced RemoteOK check with better filtering"""
        jobs = []
        try:
            print("🔍 RemoteOK Enhanced Scan...")
            
            url = "https://remoteok.io/api"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'application/json'
            }
            
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code == 200:
                data = response.json()
                
                # Enhanced testing keywords
                testing_keywords = [
                    'test', 'testing', 'qa', 'quality assurance', 'automation',
                    'selenium', 'cypress', 'junit', 'pytest', 'tester', 'sdet',
                    'quality engineer', 'test engineer', 'automation engineer',
                    'functional testing', 'regression testing', 'api testing',
                    'performance testing', 'manual testing', 'test automation',
                    'quality analyst', 'test analyst', 'software testing'
                ]
                
                for job in data[1:30]:  # Check more jobs
                    position = job.get('position', '').lower()
                    description = job.get('description', '').lower()
                    tags = [tag.lower() for tag in job.get('tags', [])]
                    
                    # Enhanced filtering
                    is_testing = (
                        any(keyword in position for keyword in testing_keywords) or
                        any(keyword in description for keyword in testing_keywords) or
                        any(keyword in tag for keyword in testing_keywords for tag in tags)
                    )
                    
                    if is_testing:
                        job_id = f"remoteok_enhanced_{job.get('id', '')}"
                        
                        if job_id not in self.tracked_jobs:
                            job_data = {
                                'id': job_id,
                                'title': job.get('position', 'N/A'),
                                'company': job.get('company', 'N/A'),
                                'location': 'Remote',
                                'snippet': job.get('description', 'N/A')[:300],
                                'url': f"https://remoteok.io/remote-jobs/{job.get('id', '')}",
                                'source': 'RemoteOK',
                                'tags': job.get('tags', []),
                                'salary': job.get('salary_min', 'Not specified'),
                                'date_found': datetime.datetime.now().isoformat(),
                                'posted_date': job.get('date', 'Recent')
                            }
                            jobs.append(job_data)
                
                print(f"✅ RemoteOK: {len(jobs)} NEW testing jobs")
                
        except Exception as e:
            print(f"❌ RemoteOK error: {str(e)}")
        
        return jobs
    
    def check_stackoverflow_jobs(self):
        """Check Stack Overflow job feeds"""
        jobs = []
        try:
            print("🔍 Stack Overflow Jobs...")
            
            # Using RSS feed for job search
            urls = [
                'https://stackoverflow.com/jobs/feed?q=software+testing',
                'https://stackoverflow.com/jobs/feed?q=qa+automation',
                'https://stackoverflow.com/jobs/feed?q=test+engineer'
            ]
            
            for url in urls:
                try:
                    feed = feedparser.parse(url)
                    
                    for entry in feed.entries[:5]:  # Recent entries
                        job_id = f"stackoverflow_{entry.get('id', '')}"
                        
                        if job_id not in self.tracked_jobs:
                            job_data = {
                                'id': job_id,
                                'title': entry.get('title', 'N/A'),
                                'company': entry.get('author', 'N/A'),
                                'location': 'Various',
                                'snippet': entry.get('summary', 'N/A')[:300],
                                'url': entry.get('link', ''),
                                'source': 'Stack Overflow',
                                'date_found': datetime.datetime.now().isoformat(),
                                'posted_date': entry.get('published', 'Recent')
                            }
                            jobs.append(job_data)
                            
                except Exception as e:
                    print(f"⚠️ Stack Overflow feed error: {str(e)}")
            
            print(f"✅ Stack Overflow: {len(jobs)} NEW jobs")
            
        except Exception as e:
            print(f"❌ Stack Overflow error: {str(e)}")
        
        return jobs
    
    def check_weworkremotely_rss(self):
        """Check WeWorkRemotely RSS feeds"""
        jobs = []
        try:
            print("🔍 WeWorkRemotely RSS...")
            
            # WeWorkRemotely RSS feeds
            rss_urls = [
                'https://weworkremotely.com/categories/remote-programming-jobs.rss',
                'https://weworkremotely.com/categories/remote-dev-ops-sysadmin-jobs.rss'
            ]
            
            testing_keywords = ['test', 'qa', 'quality', 'automation', 'sdet']
            
            for rss_url in rss_urls:
                try:
                    feed = feedparser.parse(rss_url)
                    
                    for entry in feed.entries[:10]:
                        title = entry.get('title', '').lower()
                        description = entry.get('description', '').lower()
                        
                        if any(keyword in title or keyword in description for keyword in testing_keywords):
                            job_id = f"weworkremotely_{entry.get('id', '')}"
                            
                            if job_id not in self.tracked_jobs:
                                job_data = {
                                    'id': job_id,
                                    'title': entry.get('title', 'N/A'),
                                    'company': 'Various Companies',
                                    'location': 'Remote',
                                    'snippet': entry.get('description', 'N/A')[:300],
                                    'url': entry.get('link', ''),
                                    'source': 'WeWorkRemotely',
                                    'date_found': datetime.datetime.now().isoformat(),
                                    'posted_date': entry.get('published', 'Recent')
                                }
                                jobs.append(job_data)
                                
                except Exception as e:
                    print(f"⚠️ WeWorkRemotely RSS error: {str(e)}")
            
            print(f"✅ WeWorkRemotely: {len(jobs)} NEW jobs")
            
        except Exception as e:
            print(f"❌ WeWorkRemotely error: {str(e)}")
        
        return jobs
    
    def check_github_jobs(self):
        """Check GitHub Jobs API (if available)"""
        jobs = []
        try:
            print("🔍 GitHub Jobs...")
            
            # Note: GitHub Jobs was discontinued, but checking for archives
            # This is a placeholder for other job APIs
            
            print("✅ GitHub Jobs: Service discontinued")
            
        except Exception as e:
            print(f"❌ GitHub Jobs error: {str(e)}")
        
        return jobs
    
    def send_instant_alert(self, new_jobs):
        """Send instant alert with enhanced formatting"""
        if not new_jobs:
            return False
            
        try:
            self.scan_count += 1
            current_time = datetime.datetime.now()
            
            # Create enhanced alert message
            alert_message = f"🚨 **REAL-TIME JOB ALERT #{self.scan_count}** 🚨\n\n"
            alert_message += f"🎯 **{len(new_jobs)} NEW Testing Jobs Found!**\n"
            alert_message += f"⏰ **Time**: {current_time.strftime('%H:%M:%S')}\n"
            alert_message += f"📅 **Date**: {current_time.strftime('%Y-%m-%d')}\n\n"
            
            # Group jobs by source
            sources = {}
            for job in new_jobs:
                source = job['source']
                if source not in sources:
                    sources[source] = []
                sources[source].append(job)
            
            alert_message += f"📊 **Sources**: {', '.join(sources.keys())}\n\n"
            
            # Show top jobs
            for i, job in enumerate(new_jobs[:4], 1):
                alert_message += f"**{i}. {job['title']}**\n"
                alert_message += f"🏢 **Company**: {job['company']}\n"
                alert_message += f"📍 **Location**: {job['location']}\n"
                alert_message += f"🌐 **Source**: {job['source']}\n"
                
                if job.get('salary') and job['salary'] != 'Not specified':
                    alert_message += f"💰 **Salary**: {job['salary']}\n"
                
                alert_message += f"🔗 [**APPLY NOW**]({job['url']})\n\n"
            
            if len(new_jobs) > 4:
                alert_message += f"➕ **{len(new_jobs) - 4} more jobs** available!\n\n"
            
            alert_message += f"✅ **All jobs are REAL** - No demos or samples!\n"
            alert_message += f"🔄 **Next scan** in 2 minutes"
            
            # Send to Telegram
            telegram_url = f"https://api.telegram.org/bot{self.telegram_config['bot_token']}/sendMessage"
            data = {
                'chat_id': self.telegram_config['chat_id'],
                'text': alert_message,
                'parse_mode': 'Markdown',
                'disable_web_page_preview': False
            }
            
            response = requests.post(telegram_url, data=data, timeout=10)
            
            if response.status_code == 200:
                print(f"📱 INSTANT ALERT #{self.scan_count} sent with {len(new_jobs)} jobs!")
                return True
            else:
                print(f"❌ Alert failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error sending instant alert: {str(e)}")
            return False
    
    def enhanced_real_time_scan(self):
        """Enhanced real-time scan with multiple sources"""
        print(f"\n🔄 ENHANCED SCAN #{self.scan_count + 1} - {datetime.datetime.now().strftime('%H:%M:%S')}")
        print("=" * 70)
        
        all_new_jobs = []
        
        # All job sources
        sources = [
            self.check_remoteok_enhanced,
            self.check_stackoverflow_jobs,
            self.check_weworkremotely_rss,
            self.check_github_jobs
        ]
        
        # Check all sources concurrently
        with ThreadPoolExecutor(max_workers=4) as executor:
            future_to_source = {executor.submit(source): source.__name__ for source in sources}
            
            for future in future_to_source:
                try:
                    jobs = future.result(timeout=20)
                    
                    for job in jobs:
                        if job['id'] not in self.tracked_jobs:
                            self.tracked_jobs[job['id']] = job
                            all_new_jobs.append(job)
                            
                except Exception as e:
                    source_name = future_to_source[future]
                    print(f"❌ {source_name} error: {str(e)}")
        
        if all_new_jobs:
            print(f"\n🎉 FOUND {len(all_new_jobs)} NEW REAL JOBS!")
            
            # Send instant alert
            self.send_instant_alert(all_new_jobs)
            
            # Save jobs
            self.save_tracked_jobs()
            
            # Print summary
            for job in all_new_jobs:
                print(f"✅ NEW: {job['title']} at {job['company']} ({job['source']})")
                
        else:
            print("ℹ️ No new jobs in this scan")
        
        return len(all_new_jobs)
    
    def continuous_monitoring(self, duration_minutes=60):
        """Run continuous monitoring for specified duration"""
        print("🚀 STARTING ENHANCED REAL-TIME MONITORING")
        print(f"⏱️ Duration: {duration_minutes} minutes")
        print("📱 Instant Telegram alerts: ENABLED")
        print("🔄 Scanning every 2 minutes")
        print("=" * 70)
        
        start_time = time.time()
        end_time = start_time + (duration_minutes * 60)
        
        total_jobs_found = 0
        
        try:
            while time.time() < end_time:
                new_jobs = self.enhanced_real_time_scan()
                total_jobs_found += new_jobs
                
                print(f"⏳ Waiting 2 minutes before next scan...")
                time.sleep(120)  # Wait 2 minutes
                
        except KeyboardInterrupt:
            print("\n⏹️ Monitoring stopped by user")
        
        print(f"\n📊 MONITORING SUMMARY:")
        print(f"⏱️ Duration: {duration_minutes} minutes")
        print(f"🔢 Total scans: {self.scan_count}")
        print(f"🎯 Total new jobs found: {total_jobs_found}")
        print(f"📱 Alerts sent: {self.scan_count}")

def main():
    print("🚨 ENHANCED REAL-TIME JOB MONITOR")
    print("=" * 60)
    
    # Configuration
    email_config = {
        'sender_email': 'kalyogyogi@gmail.com',
        'app_password': os.environ.get('EMAIL_APP_PASSWORD'),
        'recipient_email': 'kalyogyogi@gmail.com'
    }
    
    telegram_config = {
        'bot_token': os.environ.get('TELEGRAM_BOT_TOKEN', '8305949318:AAF257TSUv4EObGWLAAi7Cq7K87iambC9EM'),
        'chat_id': os.environ.get('TELEGRAM_CHAT_ID', '6411380646')
    }
    
    if not all(telegram_config.values()):
        print("❌ Telegram configuration missing!")
        return
    
    print("📱 Telegram: READY")
    print("🔍 Sources: RemoteOK, Stack Overflow, WeWorkRemotely, RSS Feeds")
    
    # Create monitor
    monitor = EnhancedRealTimeMonitor(email_config, telegram_config)
    
    # Run one test scan first
    print("\n🧪 Running test scan...")
    test_jobs = monitor.enhanced_real_time_scan()
    
    if test_jobs > 0:
        print(f"✅ Test successful! Found {test_jobs} jobs")
        
        # Ask for continuous monitoring
        print(f"\n🚀 Ready for continuous monitoring!")
        print("Run this script to start 24/7 monitoring:")
        print("python enhanced_realtime_monitor.py")
    else:
        print("ℹ️ Test complete - no new jobs in this scan")

if __name__ == "__main__":
    main()
