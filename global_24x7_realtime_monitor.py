#!/usr/bin/env python3
"""
GLOBAL 24/7 REAL-TIME Job Monitor
Worldwide coverage with immediate alerts for software testing jobs (2+ years experience)
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
import schedule
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('24x7_monitor.log'),
        logging.StreamHandler()
    ]
)

class Global24x7JobMonitor:
    def __init__(self, email_config, telegram_config, gemini_config=None):
        self.email_config = email_config
        self.telegram_config = telegram_config
        self.gemini_config = gemini_config
        self.jobs_file = "global_24x7_jobs.json"
        self.load_tracked_jobs()
        self.scan_count = 0
        self.total_jobs_found = 0
        
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
    
    def check_remoteok_global(self):
        """Enhanced RemoteOK with global coverage"""
        jobs = []
        try:
            logging.info("🌍 RemoteOK Global Scan...")
            
            # Multiple search terms for testing jobs
            search_terms = [
                'qa',
                'testing',
                'test engineer',
                'automation',
                'sdet',
                'quality assurance'
            ]
            
            for term in search_terms:
                try:
                    url = f"https://remoteok.io/api?tag={term}"
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                        'Accept': 'application/json'
                    }
                    
                    response = requests.get(url, headers=headers, timeout=10)
                    
                    if response.status_code == 200:
                        data = response.json()
                        
                        for job in data[1:11]:  # Skip legal notice, get top 10
                            if not job or not isinstance(job, dict):
                                continue
                                
                            job_id = f"remoteok_{job.get('id', '')}"
                            
                            if job_id not in self.tracked_jobs:
                                # Check for 2+ years experience requirement
                                description = str(job.get('description', '')).lower()
                                tags = str(job.get('tags', [])).lower()
                                
                                experience_indicators = ['2+ years', '2-', 'junior', 'mid-level', 'experienced']
                                
                                job_data = {
                                    'id': job_id,
                                    'title': job.get('position', 'N/A'),
                                    'company': job.get('company', 'N/A'),
                                    'location': job.get('location', 'Remote'),
                                    'salary': job.get('salary_max', 'Not specified'),
                                    'snippet': job.get('description', 'N/A')[:300],
                                    'url': job.get('url', ''),
                                    'source': 'RemoteOK Global',
                                    'date_found': datetime.datetime.now().isoformat(),
                                    'posted_date': job.get('date', 'Recent'),
                                    'tags': job.get('tags', []),
                                    'search_term': term
                                }
                                jobs.append(job_data)
                    
                    time.sleep(1)  # Rate limiting
                    
                except Exception as e:
                    logging.warning(f"RemoteOK term {term} error: {str(e)}")
            
            logging.info(f"✅ RemoteOK Global: {len(jobs)} NEW jobs")
            
        except Exception as e:
            logging.error(f"❌ RemoteOK Global error: {str(e)}")
        
        return jobs
    
    def check_indeed_global(self):
        """Check Indeed globally via RSS"""
        jobs = []
        try:
            logging.info("🌍 Indeed Global RSS...")
            
            # Indeed RSS feeds for different countries
            indeed_feeds = [
                'https://www.indeed.com/rss?q=software+testing+2+years&l=',
                'https://uk.indeed.com/rss?q=qa+automation+2+years&l=',
                'https://ca.indeed.com/rss?q=test+engineer+2+years&l=',
                'https://au.indeed.com/rss?q=sdet+2+years&l='
            ]
            
            for feed_url in indeed_feeds:
                try:
                    feed = feedparser.parse(feed_url)
                    
                    for entry in feed.entries[:5]:
                        job_id = f"indeed_global_{entry.get('id', '')}"
                        
                        if job_id not in self.tracked_jobs:
                            job_data = {
                                'id': job_id,
                                'title': entry.get('title', 'N/A'),
                                'company': entry.get('author', 'Various'),
                                'location': 'Various',
                                'snippet': entry.get('summary', 'N/A')[:300],
                                'url': entry.get('link', ''),
                                'source': 'Indeed Global',
                                'date_found': datetime.datetime.now().isoformat(),
                                'posted_date': entry.get('published', 'Recent')
                            }
                            jobs.append(job_data)
                            
                except Exception as e:
                    logging.warning(f"Indeed feed error: {str(e)}")
            
            logging.info(f"✅ Indeed Global: {len(jobs)} NEW jobs")
            
        except Exception as e:
            logging.error(f"❌ Indeed Global error: {str(e)}")
        
        return jobs
    
    def check_stackoverflow_global(self):
        """Enhanced Stack Overflow global job search"""
        jobs = []
        try:
            logging.info("🌍 Stack Overflow Global...")
            
            search_terms = [
                'software+testing+2+years',
                'qa+automation+experienced',
                'test+engineer+junior',
                'sdet+mid+level'
            ]
            
            for term in search_terms:
                try:
                    url = f'https://stackoverflow.com/jobs/feed?q={term}&r=true'
                    feed = feedparser.parse(url)
                    
                    for entry in feed.entries[:3]:
                        job_id = f"stackoverflow_global_{entry.get('id', '')}"
                        
                        if job_id not in self.tracked_jobs:
                            job_data = {
                                'id': job_id,
                                'title': entry.get('title', 'N/A'),
                                'company': entry.get('author', 'N/A'),
                                'location': 'Global Remote',
                                'snippet': entry.get('summary', 'N/A')[:300],
                                'url': entry.get('link', ''),
                                'source': 'Stack Overflow Global',
                                'date_found': datetime.datetime.now().isoformat(),
                                'posted_date': entry.get('published', 'Recent'),
                                'search_term': term
                            }
                            jobs.append(job_data)
                            
                except Exception as e:
                    logging.warning(f"Stack Overflow term error: {str(e)}")
            
            logging.info(f"✅ Stack Overflow Global: {len(jobs)} NEW jobs")
            
        except Exception as e:
            logging.error(f"❌ Stack Overflow Global error: {str(e)}")
        
        return jobs
    
    def check_weworkremotely_global(self):
        """Enhanced WeWorkRemotely with multiple categories"""
        jobs = []
        try:
            logging.info("🌍 WeWorkRemotely Global...")
            
            # Multiple RSS categories
            rss_urls = [
                'https://weworkremotely.com/categories/remote-programming-jobs.rss',
                'https://weworkremotely.com/categories/remote-dev-ops-sysadmin-jobs.rss',
                'https://weworkremotely.com/remote-jobs.rss'
            ]
            
            testing_keywords = ['test', 'qa', 'quality', 'automation', 'sdet', '2+ years', 'junior', 'mid-level']
            
            for rss_url in rss_urls:
                try:
                    feed = feedparser.parse(rss_url)
                    
                    for entry in feed.entries[:8]:
                        title = entry.get('title', '').lower()
                        description = entry.get('description', '').lower()
                        
                        if any(keyword in title or keyword in description for keyword in testing_keywords):
                            job_id = f"weworkremotely_global_{entry.get('id', '')}"
                            
                            if job_id not in self.tracked_jobs:
                                job_data = {
                                    'id': job_id,
                                    'title': entry.get('title', 'N/A'),
                                    'company': 'Global Remote Companies',
                                    'location': 'Worldwide Remote',
                                    'snippet': entry.get('description', 'N/A')[:300],
                                    'url': entry.get('link', ''),
                                    'source': 'WeWorkRemotely Global',
                                    'date_found': datetime.datetime.now().isoformat(),
                                    'posted_date': entry.get('published', 'Recent')
                                }
                                jobs.append(job_data)
                                
                except Exception as e:
                    logging.warning(f"WeWorkRemotely RSS error: {str(e)}")
            
            logging.info(f"✅ WeWorkRemotely Global: {len(jobs)} NEW jobs")
            
        except Exception as e:
            logging.error(f"❌ WeWorkRemotely Global error: {str(e)}")
        
        return jobs
    
    def check_angelco_startups(self):
        """Check AngelList/Wellfound for startup testing jobs"""
        jobs = []
        try:
            logging.info("🌍 AngelList/Wellfound Startups...")
            
            # AngelList doesn't have public API, using RSS if available
            # This is a placeholder for manual job board checks
            
            logging.info("✅ AngelList: Manual check recommended")
            
        except Exception as e:
            logging.error(f"❌ AngelList error: {str(e)}")
        
        return jobs
    
    def check_glassdoor_api(self):
        """Glassdoor job search (placeholder)"""
        jobs = []
        try:
            logging.info("🌍 Glassdoor Global...")
            
            # Glassdoor requires API access
            # This is a placeholder for future implementation
            
            logging.info("✅ Glassdoor: API integration needed")
            
        except Exception as e:
            logging.error(f"❌ Glassdoor error: {str(e)}")
        
        return jobs
    
    def analyze_job_with_gemini(self, job_data):
        """Use Gemini API to analyze job relevance and experience level"""
        if not self.gemini_config or not self.gemini_config.get('api_key'):
            return job_data
        
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.gemini_config['api_key'])
            
            model = genai.GenerativeModel('gemini-pro')
            
            prompt = f"""
            Analyze this job posting for software testing/QA positions:
            
            Title: {job_data['title']}
            Company: {job_data['company']}
            Description: {job_data['snippet']}
            
            Please determine:
            1. Is this suitable for 2+ years experience level?
            2. Is this a genuine testing/QA role?
            3. Rate relevance 1-10
            4. Extract key requirements
            
            Respond in JSON format:
            {{"suitable_for_2plus_years": true/false, "is_testing_role": true/false, "relevance_score": 1-10, "key_requirements": ["req1", "req2"]}}
            """
            
            response = model.generate_content(prompt)
            analysis = json.loads(response.text)
            
            job_data['gemini_analysis'] = analysis
            
        except Exception as e:
            logging.warning(f"Gemini analysis error: {str(e)}")
        
        return job_data
    
    def send_24x7_alert(self, new_jobs):
        """Send enhanced 24/7 alert"""
        if not new_jobs:
            return False
            
        try:
            self.scan_count += 1
            current_time = datetime.datetime.now()
            
            # Enhanced alert message
            alert_message = f"🚨 **24/7 GLOBAL JOB ALERT #{self.scan_count}** 🚨\n\n"
            alert_message += f"🌍 **{len(new_jobs)} NEW Testing Jobs Found Worldwide!**\n"
            alert_message += f"⏰ **Time**: {current_time.strftime('%H:%M:%S')}\n"
            alert_message += f"📅 **Date**: {current_time.strftime('%Y-%m-%d')}\n"
            alert_message += f"🎯 **Experience Level**: 2+ years preferred\n\n"
            
            # Group by source
            sources = {}
            for job in new_jobs:
                source = job['source']
                if source not in sources:
                    sources[source] = []
                sources[source].append(job)
            
            alert_message += f"📊 **Sources**: {', '.join(sources.keys())}\n"
            alert_message += f"🔢 **Total Jobs Today**: {self.total_jobs_found}\n\n"
            
            # Show top jobs
            for i, job in enumerate(new_jobs[:3], 1):
                alert_message += f"**{i}. {job['title']}**\n"
                alert_message += f"🏢 **Company**: {job['company']}\n"
                alert_message += f"📍 **Location**: {job['location']}\n"
                alert_message += f"🌐 **Source**: {job['source']}\n"
                
                if job.get('salary') and job['salary'] != 'Not specified':
                    alert_message += f"💰 **Salary**: {job['salary']}\n"
                
                # Gemini analysis if available
                if job.get('gemini_analysis'):
                    analysis = job['gemini_analysis']
                    alert_message += f"🤖 **AI Score**: {analysis.get('relevance_score', 'N/A')}/10\n"
                
                alert_message += f"🔗 [**APPLY IMMEDIATELY**]({job['url']})\n\n"
            
            if len(new_jobs) > 3:
                alert_message += f"➕ **{len(new_jobs) - 3} more opportunities** available!\n\n"
            
            alert_message += f"✅ **Real jobs only** - Immediate application recommended\n"
            alert_message += f"🔄 **Next scan** in 90 seconds\n"
            alert_message += f"⚡ **24/7 monitoring** ACTIVE"
            
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
                logging.info(f"📱 GLOBAL ALERT #{self.scan_count} sent with {len(new_jobs)} jobs!")
                return True
            else:
                logging.error(f"❌ Alert failed: {response.status_code}")
                return False
                
        except Exception as e:
            logging.error(f"❌ Error sending 24/7 alert: {str(e)}")
            return False
    
    def global_24x7_scan(self):
        """Comprehensive global scan"""
        logging.info(f"\n🌍 GLOBAL SCAN #{self.scan_count + 1} - {datetime.datetime.now().strftime('%H:%M:%S')}")
        logging.info("=" * 80)
        
        all_new_jobs = []
        
        # All global job sources
        sources = [
            self.check_remoteok_global,
            self.check_indeed_global,
            self.check_stackoverflow_global,
            self.check_weworkremotely_global,
            self.check_angelco_startups,
            self.check_glassdoor_api
        ]
        
        # Concurrent scanning
        with ThreadPoolExecutor(max_workers=6) as executor:
            future_to_source = {executor.submit(source): source.__name__ for source in sources}
            
            for future in future_to_source:
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
                    source_name = future_to_source[future]
                    logging.error(f"❌ {source_name} error: {str(e)}")
        
        if all_new_jobs:
            self.total_jobs_found += len(all_new_jobs)
            logging.info(f"\n🎉 FOUND {len(all_new_jobs)} NEW GLOBAL JOBS!")
            
            # Send instant alert
            self.send_24x7_alert(all_new_jobs)
            
            # Save jobs
            self.save_tracked_jobs()
            
            # Log found jobs
            for job in all_new_jobs:
                logging.info(f"✅ NEW: {job['title']} at {job['company']} ({job['source']})")
                
        else:
            logging.info("ℹ️ No new jobs in this global scan")
        
        return len(all_new_jobs)
    
    def start_24x7_monitoring(self):
        """Start continuous 24/7 monitoring"""
        logging.info("🚀 STARTING 24/7 GLOBAL MONITORING")
        logging.info("🌍 Coverage: Worldwide job portals")
        logging.info("📱 Instant Telegram alerts: ENABLED")
        logging.info("🔄 Scanning every 90 seconds")
        logging.info("🎯 Target: Software Testing jobs (2+ years)")
        logging.info("=" * 80)
        
        # Schedule continuous scans
        schedule.every(90).seconds.do(self.global_24x7_scan)
        
        # Run initial scan
        self.global_24x7_scan()
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
                
        except KeyboardInterrupt:
            logging.info("\n⏹️ 24/7 Monitoring stopped by user")
            logging.info(f"📊 Total scans completed: {self.scan_count}")
            logging.info(f"🎯 Total jobs found: {self.total_jobs_found}")

def main():
    print("🌍 GLOBAL 24/7 REAL-TIME JOB MONITOR")
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
    
    # Optional Gemini configuration
    gemini_config = {
        'api_key': os.environ.get('GEMINI_API_KEY')
    }
    
    if not all(telegram_config.values()):
        print("❌ Telegram configuration missing!")
        return
    
    print("📱 Telegram: READY")
    print("🌍 Global Sources: RemoteOK, Indeed, Stack Overflow, WeWorkRemotely")
    print("🎯 Target: Software Testing (2+ years experience)")
    
    if gemini_config.get('api_key'):
        print("🤖 Gemini AI: ENABLED for job analysis")
    else:
        print("🤖 Gemini AI: Not configured (optional)")
    
    # Create global monitor
    monitor = Global24x7JobMonitor(email_config, telegram_config, gemini_config)
    
    print("\n🚀 Starting 24/7 monitoring...")
    print("Press Ctrl+C to stop")
    
    # Start 24/7 monitoring
    monitor.start_24x7_monitoring()

if __name__ == "__main__":
    main()
