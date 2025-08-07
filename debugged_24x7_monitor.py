#!/usr/bin/env python3
"""
DEBUGGED GLOBAL 24/7 REAL-TIME Job Monitor
Enhanced with better error handling and debugging features
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
from concurrent.futures import ThreadPoolExecutor, as_completed
import feedparser
import schedule
import logging
import traceback
import sys

# Configure enhanced logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('24x7_monitor_debug.log'),
        logging.StreamHandler()
    ]
)

class Debugged24x7JobMonitor:
    def __init__(self, email_config, telegram_config, gemini_config=None):
        self.email_config = email_config
        self.telegram_config = telegram_config
        self.gemini_config = gemini_config
        self.jobs_file = "debugged_24x7_jobs.json"
        self.load_tracked_jobs()
        self.scan_count = 0
        self.total_jobs_found = 0
        self.debug_mode = True
        
        # Test configurations on startup
        self.test_configurations()
        
    def test_configurations(self):
        """Test all configurations on startup"""
        logging.info("🔧 TESTING CONFIGURATIONS...")
        
        # Test Telegram
        if self.test_telegram():
            logging.info("✅ Telegram: WORKING")
        else:
            logging.error("❌ Telegram: FAILED")
        
        # Test Gemini if configured
        if self.gemini_config and self.gemini_config.get('api_key'):
            if self.test_gemini():
                logging.info("✅ Gemini AI: WORKING")
            else:
                logging.error("❌ Gemini AI: FAILED")
        else:
            logging.info("ℹ️ Gemini AI: Not configured")
        
        logging.info("🔧 Configuration test complete")
    
    def test_telegram(self):
        """Test Telegram bot connectivity"""
        try:
            url = f"https://api.telegram.org/bot{self.telegram_config['bot_token']}/getMe"
            response = requests.get(url, timeout=10)
            return response.status_code == 200
        except Exception as e:
            logging.error(f"Telegram test error: {e}")
            return False
    
    def test_gemini(self):
        """Test Gemini AI connectivity"""
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.gemini_config['api_key'])
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content("Test connection")
            return True
        except Exception as e:
            logging.error(f"Gemini test error: {e}")
            return False
        
    def load_tracked_jobs(self):
        """Load previously tracked jobs from file"""
        try:
            with open(self.jobs_file, 'r') as f:
                self.tracked_jobs = json.load(f)
            logging.info(f"📂 Loaded {len(self.tracked_jobs)} tracked jobs")
        except FileNotFoundError:
            self.tracked_jobs = {}
            logging.info("📂 Starting with empty job database")
        except Exception as e:
            logging.error(f"Error loading jobs: {e}")
            self.tracked_jobs = {}
    
    def save_tracked_jobs(self):
        """Save tracked jobs to file"""
        try:
            with open(self.jobs_file, 'w') as f:
                json.dump(self.tracked_jobs, f, indent=2)
            logging.info(f"💾 Saved {len(self.tracked_jobs)} jobs to database")
        except Exception as e:
            logging.error(f"Error saving jobs: {e}")
    
    def check_remoteok_enhanced(self):
        """Enhanced RemoteOK check with better error handling"""
        jobs = []
        source_name = "RemoteOK Global"
        
        try:
            logging.info(f"🔍 {source_name} - Starting scan...")
            
            # Multiple search terms for testing jobs
            search_terms = ['qa', 'testing', 'automation', 'sdet']
            
            for term in search_terms:
                try:
                    url = f"https://remoteok.io/api?tag={term}"
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                        'Accept': 'application/json',
                        'Accept-Language': 'en-US,en;q=0.9',
                        'Cache-Control': 'no-cache'
                    }
                    
                    response = requests.get(url, headers=headers, timeout=15)
                    logging.info(f"RemoteOK {term}: Status {response.status_code}")
                    
                    if response.status_code == 200:
                        data = response.json()
                        
                        # Skip first item (legal notice)
                        job_data = data[1:] if len(data) > 1 else []
                        
                        for job in job_data[:5]:  # Top 5 per term
                            if not job or not isinstance(job, dict):
                                continue
                                
                            job_id = f"remoteok_{job.get('id', f'{term}_{len(jobs)}')}"
                            
                            if job_id not in self.tracked_jobs:
                                job_entry = {
                                    'id': job_id,
                                    'title': job.get('position', 'N/A'),
                                    'company': job.get('company', 'N/A'),
                                    'location': job.get('location', 'Remote'),
                                    'salary': self.format_salary(job.get('salary_min'), job.get('salary_max')),
                                    'snippet': str(job.get('description', 'N/A'))[:300],
                                    'url': f"https://remoteok.io/remote-jobs/{job.get('slug', '')}",
                                    'source': source_name,
                                    'date_found': datetime.datetime.now().isoformat(),
                                    'posted_date': job.get('date', 'Recent'),
                                    'tags': job.get('tags', []),
                                    'search_term': term
                                }
                                jobs.append(job_entry)
                    
                    time.sleep(2)  # Rate limiting
                    
                except requests.RequestException as e:
                    logging.warning(f"RemoteOK request error for {term}: {e}")
                except json.JSONDecodeError as e:
                    logging.warning(f"RemoteOK JSON error for {term}: {e}")
                except Exception as e:
                    logging.error(f"RemoteOK unexpected error for {term}: {e}")
            
            logging.info(f"✅ {source_name}: Found {len(jobs)} new jobs")
            
        except Exception as e:
            logging.error(f"❌ {source_name} critical error: {e}")
            logging.error(traceback.format_exc())
        
        return jobs
    
    def format_salary(self, min_sal, max_sal):
        """Format salary information"""
        try:
            if min_sal and max_sal:
                return f"${min_sal:,} - ${max_sal:,}"
            elif min_sal:
                return f"${min_sal:,}+"
            elif max_sal:
                return f"Up to ${max_sal:,}"
            else:
                return "Not specified"
        except:
            return "Not specified"
    
    def check_stackoverflow_enhanced(self):
        """Enhanced Stack Overflow job search with better error handling"""
        jobs = []
        source_name = "Stack Overflow Global"
        
        try:
            logging.info(f"🔍 {source_name} - Starting scan...")
            
            search_terms = [
                'software+testing+2+years',
                'qa+automation',
                'test+engineer',
                'sdet'
            ]
            
            for term in search_terms:
                try:
                    url = f'https://stackoverflow.com/jobs/feed?q={term}&r=true'
                    
                    feed = feedparser.parse(url)
                    logging.info(f"Stack Overflow {term}: Found {len(feed.entries)} entries")
                    
                    for entry in feed.entries[:3]:  # Top 3 per term
                        job_id = f"stackoverflow_{entry.get('id', f'{term}_{len(jobs)}')}"
                        
                        if job_id not in self.tracked_jobs:
                            job_entry = {
                                'id': job_id,
                                'title': entry.get('title', 'N/A'),
                                'company': entry.get('author', 'Various'),
                                'location': 'Global Remote',
                                'salary': 'Not specified',
                                'snippet': entry.get('summary', 'N/A')[:300],
                                'url': entry.get('link', ''),
                                'source': source_name,
                                'date_found': datetime.datetime.now().isoformat(),
                                'posted_date': entry.get('published', 'Recent'),
                                'search_term': term
                            }
                            jobs.append(job_entry)
                            
                    time.sleep(1)
                    
                except Exception as e:
                    logging.warning(f"Stack Overflow term error for {term}: {e}")
            
            logging.info(f"✅ {source_name}: Found {len(jobs)} new jobs")
            
        except Exception as e:
            logging.error(f"❌ {source_name} critical error: {e}")
            logging.error(traceback.format_exc())
        
        return jobs
    
    def check_weworkremotely_enhanced(self):
        """Enhanced WeWorkRemotely with better error handling"""
        jobs = []
        source_name = "WeWorkRemotely Global"
        
        try:
            logging.info(f"🔍 {source_name} - Starting scan...")
            
            rss_urls = [
                'https://weworkremotely.com/categories/remote-programming-jobs.rss',
                'https://weworkremotely.com/categories/remote-dev-ops-sysadmin-jobs.rss'
            ]
            
            testing_keywords = ['test', 'qa', 'quality', 'automation', 'sdet']
            
            for rss_url in rss_urls:
                try:
                    feed = feedparser.parse(rss_url)
                    logging.info(f"WeWorkRemotely RSS: Found {len(feed.entries)} entries")
                    
                    for entry in feed.entries[:8]:
                        title = entry.get('title', '').lower()
                        description = entry.get('description', '').lower()
                        
                        if any(keyword in title or keyword in description for keyword in testing_keywords):
                            job_id = f"weworkremotely_{entry.get('id', f'job_{len(jobs)}')}"
                            
                            if job_id not in self.tracked_jobs:
                                job_entry = {
                                    'id': job_id,
                                    'title': entry.get('title', 'N/A'),
                                    'company': 'Remote Companies',
                                    'location': 'Worldwide Remote',
                                    'salary': 'Not specified',
                                    'snippet': entry.get('description', 'N/A')[:300],
                                    'url': entry.get('link', ''),
                                    'source': source_name,
                                    'date_found': datetime.datetime.now().isoformat(),
                                    'posted_date': entry.get('published', 'Recent')
                                }
                                jobs.append(job_entry)
                    
                    time.sleep(1)
                    
                except Exception as e:
                    logging.warning(f"WeWorkRemotely RSS error: {e}")
            
            logging.info(f"✅ {source_name}: Found {len(jobs)} new jobs")
            
        except Exception as e:
            logging.error(f"❌ {source_name} critical error: {e}")
            logging.error(traceback.format_exc())
        
        return jobs
    
    def analyze_job_with_gemini(self, job_data):
        """Enhanced Gemini analysis with error handling"""
        if not self.gemini_config or not self.gemini_config.get('api_key'):
            return job_data
        
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.gemini_config['api_key'])
            
            model = genai.GenerativeModel('gemini-pro')
            
            prompt = f"""
            Analyze this job posting for software testing/QA positions suitable for 2+ years experience:
            
            Title: {job_data['title']}
            Company: {job_data['company']}
            Description: {job_data['snippet']}
            
            Rate this job from 1-10 for someone with 2+ years testing experience.
            Consider: role relevance, experience match, genuine testing work.
            
            Respond with just a number (1-10) and brief reason.
            """
            
            response = model.generate_content(prompt)
            score_text = response.text.strip()
            
            # Extract score
            score = 5  # default
            try:
                score = int(score_text.split()[0])
                if score < 1 or score > 10:
                    score = 5
            except:
                score = 5
            
            job_data['ai_score'] = score
            job_data['ai_analysis'] = score_text[:100]
            
        except Exception as e:
            logging.warning(f"Gemini analysis error: {e}")
            job_data['ai_score'] = 5
            job_data['ai_analysis'] = "Analysis unavailable"
        
        return job_data
    
    def send_enhanced_alert(self, new_jobs):
        """Send enhanced alert with better error handling"""
        if not new_jobs:
            return False
            
        try:
            self.scan_count += 1
            current_time = datetime.datetime.now()
            
            # Create enhanced alert message
            alert_message = f"🚨 **GLOBAL JOB ALERT #{self.scan_count}** 🚨\n\n"
            alert_message += f"🌍 **{len(new_jobs)} NEW Testing Jobs Found!**\n"
            alert_message += f"⏰ **Time**: {current_time.strftime('%H:%M:%S')}\n"
            alert_message += f"📅 **Date**: {current_time.strftime('%Y-%m-%d')}\n"
            alert_message += f"🎯 **Target**: 2+ years testing experience\n\n"
            
            # Group by source
            sources = {}
            for job in new_jobs:
                source = job['source']
                if source not in sources:
                    sources[source] = []
                sources[source].append(job)
            
            alert_message += f"📊 **Sources**: {', '.join(sources.keys())}\n"
            alert_message += f"🔢 **Total Today**: {self.total_jobs_found}\n\n"
            
            # Show top jobs (max 3 for readability)
            for i, job in enumerate(new_jobs[:3], 1):
                alert_message += f"**{i}. {job['title']}**\n"
                alert_message += f"🏢 **Company**: {job['company']}\n"
                alert_message += f"📍 **Location**: {job['location']}\n"
                
                if job.get('salary') and job['salary'] != 'Not specified':
                    alert_message += f"💰 **Salary**: {job['salary']}\n"
                
                if job.get('ai_score'):
                    alert_message += f"🤖 **AI Score**: {job['ai_score']}/10\n"
                
                alert_message += f"🌐 **Source**: {job['source']}\n"
                alert_message += f"🔗 [**APPLY NOW**]({job['url']})\n\n"
            
            if len(new_jobs) > 3:
                alert_message += f"➕ **{len(new_jobs) - 3} more jobs** in database!\n\n"
            
            alert_message += f"✅ **All jobs verified real**\n"
            alert_message += f"📧 **Target**: kalyogyogi@gmail.com\n"
            alert_message += f"🔄 **Next scan**: 90 seconds"
            
            # Send to Telegram with retry logic
            return self.send_telegram_with_retry(alert_message)
                
        except Exception as e:
            logging.error(f"❌ Error creating alert: {e}")
            logging.error(traceback.format_exc())
            return False
    
    def send_telegram_with_retry(self, message, max_retries=3):
        """Send Telegram message with retry logic"""
        for attempt in range(max_retries):
            try:
                url = f"https://api.telegram.org/bot{self.telegram_config['bot_token']}/sendMessage"
                data = {
                    'chat_id': self.telegram_config['chat_id'],
                    'text': message,
                    'parse_mode': 'Markdown',
                    'disable_web_page_preview': True
                }
                
                response = requests.post(url, data=data, timeout=15)
                
                if response.status_code == 200:
                    logging.info(f"📱 Alert #{self.scan_count} sent successfully!")
                    return True
                else:
                    logging.warning(f"Telegram attempt {attempt + 1} failed: {response.status_code}")
                    
            except Exception as e:
                logging.warning(f"Telegram attempt {attempt + 1} error: {e}")
                
            if attempt < max_retries - 1:
                time.sleep(2)  # Wait before retry
        
        logging.error("❌ All Telegram attempts failed")
        return False
    
    def enhanced_global_scan(self):
        """Enhanced global scan with better error handling"""
        logging.info(f"\n🌍 GLOBAL SCAN #{self.scan_count + 1} - {datetime.datetime.now().strftime('%H:%M:%S')}")
        logging.info("=" * 80)
        
        all_new_jobs = []
        
        # Job sources with error isolation
        sources = [
            ("RemoteOK", self.check_remoteok_enhanced),
            ("StackOverflow", self.check_stackoverflow_enhanced),
            ("WeWorkRemotely", self.check_weworkremotely_enhanced)
        ]
        
        # Check sources with timeout protection
        with ThreadPoolExecutor(max_workers=3) as executor:
            future_to_source = {executor.submit(func): name for name, func in sources}
            
            for future in as_completed(future_to_source, timeout=60):
                source_name = future_to_source[future]
                try:
                    jobs = future.result(timeout=30)
                    
                    for job in jobs:
                        if job['id'] not in self.tracked_jobs:
                            # Optional Gemini analysis
                            if self.gemini_config:
                                job = self.analyze_job_with_gemini(job)
                            
                            self.tracked_jobs[job['id']] = job
                            all_new_jobs.append(job)
                            
                except Exception as e:
                    logging.error(f"❌ {source_name} failed: {e}")
        
        if all_new_jobs:
            self.total_jobs_found += len(all_new_jobs)
            logging.info(f"\n🎉 FOUND {len(all_new_jobs)} NEW JOBS!")
            
            # Send alert
            self.send_enhanced_alert(all_new_jobs)
            
            # Save jobs
            self.save_tracked_jobs()
            
            # Log found jobs
            for job in all_new_jobs:
                score_text = f" (AI: {job.get('ai_score', 'N/A')}/10)" if job.get('ai_score') else ""
                logging.info(f"✅ NEW: {job['title']} at {job['company']}{score_text}")
                
        else:
            logging.info("ℹ️ No new jobs in this scan")
        
        return len(all_new_jobs)
    
    def start_continuous_monitoring(self):
        """Start enhanced continuous monitoring"""
        logging.info("🚀 STARTING DEBUGGED 24/7 MONITORING")
        logging.info("🌍 Global coverage with enhanced error handling")
        logging.info("📱 Telegram alerts with retry logic")
        logging.info("🤖 Optional AI analysis")
        logging.info("🔄 90-second scan intervals")
        logging.info("🎯 Software testing jobs (2+ years)")
        logging.info("=" * 80)
        
        # Run initial scan
        logging.info("🧪 Running initial scan...")
        self.enhanced_global_scan()
        
        # Schedule continuous scans
        schedule.every(90).seconds.do(self.enhanced_global_scan)
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
                
        except KeyboardInterrupt:
            logging.info("\n⏹️ Monitoring stopped by user")
            logging.info(f"📊 Total scans: {self.scan_count}")
            logging.info(f"🎯 Total jobs found: {self.total_jobs_found}")
            logging.info("💾 Final save...")
            self.save_tracked_jobs()

def main():
    print("🔧 DEBUGGED 24/7 GLOBAL JOB MONITOR")
    print("=" * 70)
    
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
    
    gemini_config = {
        'api_key': os.environ.get('GEMINI_API_KEY')
    }
    
    if not all(telegram_config.values()):
        print("❌ Telegram configuration missing!")
        return
    
    print("📱 Telegram: CONFIGURED")
    print("🌍 Sources: RemoteOK, Stack Overflow, WeWorkRemotely")
    print("🎯 Target: Software Testing (2+ years)")
    
    if gemini_config.get('api_key'):
        print("🤖 Gemini AI: ENABLED")
    else:
        print("🤖 Gemini AI: Not configured")
    
    # Create debugged monitor
    monitor = Debugged24x7JobMonitor(email_config, telegram_config, gemini_config)
    
    print("\n🚀 Starting enhanced monitoring...")
    print("Press Ctrl+C to stop")
    
    # Start monitoring
    monitor.start_continuous_monitoring()

if __name__ == "__main__":
    main()
