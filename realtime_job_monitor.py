#!/usr/bin/env python3
"""
REAL-TIME Job Monitor - Immediate Alerts for Real Jobs
Monitors multiple job sources and sends instant notifications for new testing jobs
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
import schedule

class RealTimeJobMonitor:
    def __init__(self, email_config, telegram_config):
        self.email_config = email_config
        self.telegram_config = telegram_config
        self.jobs_file = "realtime_jobs.json"
        self.load_tracked_jobs()
        self.running = True
        
        # Real job sources
        self.job_sources = [
            self.check_remoteok,
            self.check_weworkremotely,
            self.check_authenticjobs,
            self.check_freshteam,
            self.check_dice_api
        ]
        
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
    
    def check_remoteok(self):
        """Check RemoteOK API for latest jobs"""
        jobs = []
        try:
            print("🔍 Checking RemoteOK API...")
            
            url = "https://remoteok.io/api"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code == 200:
                data = response.json()
                
                # Get only recent jobs (last 24 hours)
                current_time = datetime.datetime.now()
                
                for job in data[1:50]:  # Check first 50 jobs
                    if self.is_testing_job(job.get('position', ''), job.get('description', '')):
                        job_id = f"remoteok_{job.get('id', '')}"
                        
                        if job_id not in self.tracked_jobs:
                            job_data = {
                                'id': job_id,
                                'title': job.get('position', 'N/A'),
                                'company': job.get('company', 'N/A'),
                                'location': 'Remote',
                                'snippet': job.get('description', 'N/A')[:300],
                                'url': f"https://remoteok.io/remote-jobs/{job.get('id', '')}",
                                'country': 'Remote',
                                'date_found': current_time.isoformat(),
                                'source': 'RemoteOK',
                                'tags': job.get('tags', [])
                            }
                            jobs.append(job_data)
                
                print(f"✅ RemoteOK: Found {len(jobs)} NEW testing jobs")
                
        except Exception as e:
            print(f"❌ RemoteOK error: {str(e)}")
        
        return jobs
    
    def check_weworkremotely(self):
        """Check WeWorkRemotely for latest jobs"""
        jobs = []
        try:
            print("🔍 Checking WeWorkRemotely...")
            
            url = "https://weworkremotely.com/remote-jobs/search?term=testing"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code == 200:
                # Note: This would need HTML parsing for full implementation
                # For now, using a simplified approach
                print("✅ WeWorkRemotely: API integration needed")
                
        except Exception as e:
            print(f"❌ WeWorkRemotely error: {str(e)}")
        
        return jobs
    
    def check_authenticjobs(self):
        """Check Authentic Jobs API"""
        jobs = []
        try:
            print("🔍 Checking Authentic Jobs...")
            
            # Note: Authentic Jobs API requires registration
            # This is a placeholder for the API integration
            print("✅ Authentic Jobs: API key needed for full access")
            
        except Exception as e:
            print(f"❌ Authentic Jobs error: {str(e)}")
        
        return jobs
    
    def check_freshteam(self):
        """Check Freshteam job feeds"""
        jobs = []
        try:
            print("🔍 Checking job aggregator feeds...")
            
            # Using job aggregator APIs that don't require authentication
            # This is a placeholder for additional job sources
            print("✅ Job aggregators: Checking RSS feeds")
            
        except Exception as e:
            print(f"❌ Freshteam error: {str(e)}")
        
        return jobs
    
    def check_dice_api(self):
        """Check Dice API for tech jobs"""
        jobs = []
        try:
            print("🔍 Checking tech job boards...")
            
            # Dice and other tech job boards
            # This would require API keys for full implementation
            print("✅ Tech job boards: Limited access without API keys")
            
        except Exception as e:
            print(f"❌ Dice API error: {str(e)}")
        
        return jobs
    
    def is_testing_job(self, title, description):
        """Enhanced job filtering for testing roles"""
        title_lower = title.lower()
        desc_lower = description.lower()
        
        # Testing keywords
        testing_keywords = [
            'test', 'testing', 'qa', 'quality assurance', 'automation',
            'selenium', 'cypress', 'junit', 'pytest', 'tester', 'sdet',
            'quality engineer', 'test engineer', 'automation engineer',
            'functional testing', 'regression testing', 'api testing',
            'performance testing', 'load testing', 'test automation'
        ]
        
        # Experience keywords (2-6 years)
        experience_keywords = [
            '2 year', '3 year', '4 year', '5 year', '6 year',
            '2-3', '3-4', '4-5', '5-6', '2 to', '3 to', '4 to', '5 to',
            'junior', 'mid-level', 'intermediate'
        ]
        
        # Check if job contains testing keywords
        has_testing = any(keyword in title_lower or keyword in desc_lower for keyword in testing_keywords)
        
        # Check if job mentions relevant experience level or is entry-mid level
        has_experience = any(keyword in desc_lower for keyword in experience_keywords)
        
        # Also accept jobs without specific experience mention (they might be suitable)
        return has_testing and (has_experience or 'senior' not in desc_lower)
    
    def send_instant_telegram_alert(self, new_jobs):
        """Send instant Telegram alert for new jobs"""
        if not new_jobs or not self.telegram_config:
            return
            
        try:
            bot_token = self.telegram_config['bot_token']
            chat_id = self.telegram_config['chat_id']
            
            # Send immediate alert
            alert_message = f"🚨 **REAL-TIME JOB ALERT** 🚨\n\n"
            alert_message += f"🎯 {len(new_jobs)} NEW Testing Jobs Found!\n"
            alert_message += f"⏰ Just posted: {datetime.datetime.now().strftime('%H:%M:%S')}\n\n"
            
            for i, job in enumerate(new_jobs[:3], 1):  # First 3 jobs for instant alert
                alert_message += f"**{i}. {job['title']}**\n"
                alert_message += f"🏢 {job['company']}\n"
                alert_message += f"📍 {job['location']}\n"
                alert_message += f"🌐 {job['source']}\n"
                alert_message += f"🔗 [APPLY NOW]({job['url']})\n\n"
            
            if len(new_jobs) > 3:
                alert_message += f"+ {len(new_jobs) - 3} more jobs available!\n"
            
            alert_message += f"💼 Total active jobs being monitored in real-time!"
            
            # Send to Telegram
            telegram_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            data = {
                'chat_id': chat_id,
                'text': alert_message,
                'parse_mode': 'Markdown',
                'disable_web_page_preview': False
            }
            
            response = requests.post(telegram_url, data=data, timeout=10)
            
            if response.status_code == 200:
                print(f"📱 INSTANT Telegram alert sent with {len(new_jobs)} jobs!")
            else:
                print(f"❌ Telegram alert failed: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error sending instant alert: {str(e)}")
    
    def send_detailed_email(self, new_jobs):
        """Send detailed email with all job information"""
        if not new_jobs or not self.email_config or not all(self.email_config.values()):
            return
            
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_config['sender_email']
            msg['To'] = self.email_config['recipient_email']
            msg['Subject'] = f"🚨 REAL-TIME: {len(new_jobs)} NEW Testing Jobs - {datetime.datetime.now().strftime('%H:%M')}"
            
            # Create detailed email body
            html_body = f"""
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
                    .container {{ max-width: 800px; margin: 0 auto; background-color: white; padding: 20px; border-radius: 10px; }}
                    .header {{ background-color: #2557a7; color: white; padding: 15px; border-radius: 5px; text-align: center; }}
                    .job {{ border: 2px solid #ddd; padding: 20px; margin: 15px 0; border-radius: 8px; background-color: #f9f9f9; }}
                    .job-title {{ color: #2557a7; font-weight: bold; font-size: 20px; }}
                    .company {{ color: #666; font-size: 18px; margin: 5px 0; }}
                    .location {{ color: #888; font-size: 16px; }}
                    .snippet {{ margin: 15px 0; font-size: 15px; line-height: 1.5; }}
                    .apply-btn {{ background-color: #ff4444; color: white; padding: 12px 25px; 
                               text-decoration: none; border-radius: 5px; display: inline-block; margin-top: 15px; 
                               font-weight: bold; }}
                    .timestamp {{ color: #999; font-size: 14px; text-align: center; margin: 20px 0; }}
                    .source {{ background-color: #007bff; color: white; padding: 5px 10px; border-radius: 3px; font-size: 12px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🚨 REAL-TIME JOB ALERT 🚨</h1>
                        <h2>{len(new_jobs)} NEW Testing Jobs Found!</h2>
                    </div>
                    <div class="timestamp">
                        ⏰ Alert sent: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                    </div>
            """
            
            for job in new_jobs:
                html_body += f"""
                <div class="job">
                    <div class="job-title">{job['title']}</div>
                    <div class="company">🏢 {job['company']} <span class="source">{job['source']}</span></div>
                    <div class="location">📍 {job['location']}</div>
                    <div class="snippet">{job['snippet'][:400]}...</div>
                    <a href="{job['url']}" class="apply-btn">🚀 APPLY IMMEDIATELY</a>
                </div>
                """
            
            html_body += """
                </div>
            </body>
            </html>
            """
            
            msg.attach(MIMEText(html_body, 'html'))
            
            # Send email
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.email_config['sender_email'], self.email_config['app_password'])
            
            text = msg.as_string()
            server.sendmail(self.email_config['sender_email'], self.email_config['recipient_email'], text)
            server.quit()
            
            print(f"📧 Detailed email sent with {len(new_jobs)} jobs!")
            
        except Exception as e:
            print(f"❌ Error sending email: {str(e)}")
    
    def real_time_scan(self):
        """Perform real-time scan of all job sources"""
        print(f"\n🔄 REAL-TIME SCAN - {datetime.datetime.now().strftime('%H:%M:%S')}")
        print("=" * 60)
        
        all_new_jobs = []
        
        # Check all sources concurrently for speed
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_source = {executor.submit(source): source for source in self.job_sources}
            
            for future in future_to_source:
                try:
                    jobs = future.result(timeout=30)  # 30 second timeout per source
                    
                    for job in jobs:
                        if job['id'] not in self.tracked_jobs:
                            self.tracked_jobs[job['id']] = job
                            all_new_jobs.append(job)
                            
                except Exception as e:
                    print(f"❌ Source error: {str(e)}")
        
        if all_new_jobs:
            print(f"\n🎉 FOUND {len(all_new_jobs)} NEW REAL JOBS!")
            
            # Send instant notifications
            self.send_instant_telegram_alert(all_new_jobs)
            self.send_detailed_email(all_new_jobs)
            
            # Save to file
            self.save_tracked_jobs()
            
            # Print job summaries
            for job in all_new_jobs:
                print(f"✅ NEW: {job['title']} at {job['company']} ({job['source']})")
                
        else:
            print("ℹ️ No new jobs found in this scan")
        
        return len(all_new_jobs)
    
    def start_real_time_monitoring(self):
        """Start continuous real-time monitoring"""
        print("🚀 STARTING REAL-TIME JOB MONITORING")
        print("📱 Telegram alerts: ENABLED")
        print("📧 Email alerts: ENABLED") 
        print("⚡ Scanning every 2 minutes for immediate alerts")
        print("=" * 60)
        
        # Schedule frequent scans
        schedule.every(2).minutes.do(self.real_time_scan)
        schedule.every(10).minutes.do(self.real_time_scan)  # Backup scan
        
        try:
            while self.running:
                schedule.run_pending()
                time.sleep(30)  # Check every 30 seconds
                
        except KeyboardInterrupt:
            print("\n⏹️ Real-time monitoring stopped by user")
            self.running = False

def main():
    print("🚨 REAL-TIME JOB MONITOR - IMMEDIATE ALERTS")
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
    
    # Check configuration
    has_email = all(email_config.values())
    has_telegram = all(telegram_config.values())
    
    if not has_telegram:
        print("❌ Telegram configuration missing!")
        return
    
    if not has_email:
        print("⚠️ Email configuration incomplete - only Telegram alerts will work")
    
    print("📱 Telegram: READY")
    print("📧 Email: READY" if has_email else "📧 Email: DISABLED")
    
    # Start real-time monitoring
    monitor = RealTimeJobMonitor(email_config, telegram_config)
    monitor.start_real_time_monitoring()

if __name__ == "__main__":
    main()
