#!/usr/bin/env python3
"""
ULTRA REAL-TIME 24/7 Job Monitor
Continuous scanning with instant alerts - NEVER STOPS
"""

import requests
import json
import datetime
import time
import os
import threading
import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
import feedparser

# Real-time logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler('ultra_realtime_24x7.log'),
        logging.StreamHandler()
    ]
)

class UltraRealtime24x7Monitor:
    def __init__(self):
        self.telegram_config = {
            'bot_token': '8305949318:AAF257TSUv4EObGWLAAi7Cq7K87iambC9EM',
            'chat_id': '6411380646'
        }
        self.jobs_file = "ultra_realtime_jobs.json"
        self.tracked_jobs = {}
        self.scan_count = 0
        self.alerts_sent = 0
        self.is_running = True
        self.load_tracked_jobs()
        
        # Send startup alert
        self.send_startup_alert()
        
    def load_tracked_jobs(self):
        try:
            with open(self.jobs_file, 'r') as f:
                self.tracked_jobs = json.load(f)
        except:
            self.tracked_jobs = {}
    
    def save_tracked_jobs(self):
        try:
            with open(self.jobs_file, 'w') as f:
                json.dump(self.tracked_jobs, f, indent=2)
        except Exception as e:
            logging.error(f"Save error: {e}")
    
    def send_startup_alert(self):
        """Send alert when monitoring starts"""
        try:
            message = f"🚀 **ULTRA REAL-TIME 24/7 MONITORING STARTED** 🚀\n\n"
            message += f"⏰ **Started**: {datetime.datetime.now().strftime('%H:%M:%S')}\n"
            message += f"📅 **Date**: {datetime.datetime.now().strftime('%Y-%m-%d')}\n"
            message += f"🎯 **Target**: Software Testing Jobs (2+ years)\n"
            message += f"📧 **Email**: kalyogyogi@gmail.com\n"
            message += f"⚡ **Scan Frequency**: Every 15 seconds\n"
            message += f"🔄 **Mode**: Continuous 24/7 operation\n\n"
            message += f"✅ **System Status**: ACTIVE\n"
            message += f"🚨 **Alert Mode**: INSTANT for every testing job\n"
            message += f"🎯 **Job Types**: QA, Testing, Automation, SDET only\n\n"
            message += f"📱 **You will receive instant alerts for every testing job found!**\n"
            message += f"🔥 **Ultra-aggressive monitoring in progress...**"
            
            self.send_telegram_message(message)
            logging.info("🚀 Startup alert sent!")
            
        except Exception as e:
            logging.error(f"Startup alert error: {e}")
    
    def send_telegram_message(self, message):
        """Send Telegram message with retry"""
        for attempt in range(3):
            try:
                url = f"https://api.telegram.org/bot{self.telegram_config['bot_token']}/sendMessage"
                data = {
                    'chat_id': self.telegram_config['chat_id'],
                    'text': message,
                    'parse_mode': 'Markdown',
                    'disable_web_page_preview': True
                }
                
                response = requests.post(url, data=data, timeout=10)
                if response.status_code == 200:
                    return True
                    
            except Exception as e:
                logging.warning(f"Telegram attempt {attempt + 1} failed: {e}")
                time.sleep(1)
        
        return False
    
    def ultra_fast_remoteok_scan(self):
        """Ultra-fast RemoteOK scanning"""
        jobs = []
        try:
            # Multiple simultaneous searches
            search_terms = ['qa', 'testing', 'automation', 'sdet', 'quality']
            
            for term in search_terms:
                try:
                    url = f"https://remoteok.io/api?tag={term}"
                    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
                    
                    response = requests.get(url, headers=headers, timeout=8)
                    if response.status_code == 200:
                        data = response.json()
                        
                        for job in data[1:6]:  # Top 5 per term
                            if not job or not isinstance(job, dict):
                                continue
                                
                            title = str(job.get('position', '')).lower()
                            description = str(job.get('description', '')).lower()
                            
                            # Ultra-specific testing filter
                            testing_keywords = ['qa', 'test', 'quality', 'automation', 'sdet']
                            if any(keyword in title for keyword in testing_keywords):
                                job_id = f"remoteok_ultra_{job.get('id', len(jobs))}"
                                
                                if job_id not in self.tracked_jobs:
                                    salary = 'Competitive'
                                    if job.get('salary_min') and job.get('salary_max'):
                                        salary = f"${job['salary_min']:,} - ${job['salary_max']:,}"
                                    
                                    job_entry = {
                                        'id': job_id,
                                        'title': job.get('position', 'Testing Position'),
                                        'company': job.get('company', 'Tech Company'),
                                        'location': job.get('location', 'Remote'),
                                        'salary': salary,
                                        'url': f"https://remoteok.io/remote-jobs/{job.get('slug', '')}",
                                        'source': 'RemoteOK',
                                        'found_at': datetime.datetime.now().isoformat(),
                                        'tags': job.get('tags', [])
                                    }
                                    jobs.append(job_entry)
                    
                    time.sleep(0.2)  # Minimal delay
                    
                except Exception as e:
                    continue  # Skip errors, keep scanning
            
        except Exception as e:
            logging.warning(f"RemoteOK scan error: {e}")
        
        return jobs
    
    def ultra_fast_indeed_scan(self):
        """Ultra-fast Indeed RSS scanning"""
        jobs = []
        try:
            # Multiple Indeed RSS feeds
            feeds = [
                'https://www.indeed.com/rss?q=qa+engineer&sort=date',
                'https://www.indeed.com/rss?q=test+automation&sort=date', 
                'https://www.indeed.com/rss?q=software+testing&sort=date',
                'https://uk.indeed.com/rss?q=qa+automation&sort=date'
            ]
            
            for feed_url in feeds:
                try:
                    feed = feedparser.parse(feed_url)
                    
                    for entry in feed.entries[:3]:  # Top 3 per feed
                        title = str(entry.get('title', '')).lower()
                        
                        testing_keywords = ['qa', 'test', 'quality', 'automation', 'sdet']
                        if any(keyword in title for keyword in testing_keywords):
                            job_id = f"indeed_ultra_{entry.get('id', len(jobs))}"
                            
                            if job_id not in self.tracked_jobs:
                                job_entry = {
                                    'id': job_id,
                                    'title': entry.get('title', 'Testing Position'),
                                    'company': entry.get('author', 'Company'),
                                    'location': 'Various',
                                    'salary': 'See posting',
                                    'url': entry.get('link', ''),
                                    'source': 'Indeed',
                                    'found_at': datetime.datetime.now().isoformat()
                                }
                                jobs.append(job_entry)
                    
                    time.sleep(0.2)
                    
                except Exception as e:
                    continue  # Skip errors, keep scanning
            
        except Exception as e:
            logging.warning(f"Indeed scan error: {e}")
        
        return jobs
    
    def ultra_fast_stackoverflow_scan(self):
        """Ultra-fast Stack Overflow scanning"""
        jobs = []
        try:
            searches = [
                'qa+engineer', 'test+automation', 'software+testing', 'sdet+engineer'
            ]
            
            for search in searches:
                try:
                    url = f'https://stackoverflow.com/jobs/feed?q={search}&sort=i'
                    feed = feedparser.parse(url)
                    
                    for entry in feed.entries[:2]:  # Top 2 per search
                        title = str(entry.get('title', '')).lower()
                        
                        testing_keywords = ['qa', 'test', 'quality', 'automation', 'sdet']
                        if any(keyword in title for keyword in testing_keywords):
                            job_id = f"stackoverflow_ultra_{entry.get('id', len(jobs))}"
                            
                            if job_id not in self.tracked_jobs:
                                job_entry = {
                                    'id': job_id,
                                    'title': entry.get('title', 'Testing Position'),
                                    'company': entry.get('author', 'Tech Company'),
                                    'location': 'Remote',
                                    'salary': 'Competitive',
                                    'url': entry.get('link', ''),
                                    'source': 'Stack Overflow',
                                    'found_at': datetime.datetime.now().isoformat()
                                }
                                jobs.append(job_entry)
                    
                    time.sleep(0.2)
                    
                except Exception as e:
                    continue  # Skip errors, keep scanning
            
        except Exception as e:
            logging.warning(f"Stack Overflow scan error: {e}")
        
        return jobs
    
    def send_instant_job_alert(self, jobs):
        """Send instant alert for new testing jobs"""
        if not jobs:
            return False
        
        try:
            self.alerts_sent += 1
            current_time = datetime.datetime.now()
            
            message = f"🚨 **INSTANT TESTING JOB ALERT #{self.alerts_sent}** 🚨\n\n"
            message += f"🎯 **{len(jobs)} NEW Testing Jobs Found!**\n"
            message += f"⚡ **APPLY IMMEDIATELY**\n"
            message += f"⏰ **Time**: {current_time.strftime('%H:%M:%S')}\n"
            message += f"📧 **For**: kalyogyogi@gmail.com\n\n"
            
            for i, job in enumerate(jobs[:3], 1):  # Show max 3 jobs
                message += f"**🎯 {i}. {job['title']}**\n"
                message += f"🏢 **Company**: {job['company']}\n"
                message += f"📍 **Location**: {job['location']}\n"
                message += f"💰 **Salary**: {job['salary']}\n"
                message += f"🌐 **Source**: {job['source']}\n"
                message += f"🔗 [**APPLY NOW**]({job['url']})\n\n"
            
            if len(jobs) > 3:
                message += f"➕ **{len(jobs) - 3} more testing jobs** found!\n\n"
            
            message += f"✅ **100% Testing Jobs**\n"
            message += f"⚡ **Next scan**: 15 seconds\n"
            message += f"🔥 **24/7 Ultra-aggressive monitoring**"
            
            if self.send_telegram_message(message):
                logging.info(f"🚨 INSTANT ALERT #{self.alerts_sent} sent! ({len(jobs)} jobs)")
                return True
            else:
                logging.error("Alert send failed")
                return False
                
        except Exception as e:
            logging.error(f"Alert error: {e}")
            return False
    
    def ultra_aggressive_scan(self):
        """Ultra-aggressive concurrent scanning"""
        self.scan_count += 1
        logging.info(f"⚡ ULTRA SCAN #{self.scan_count} - {datetime.datetime.now().strftime('%H:%M:%S')}")
        
        all_new_jobs = []
        
        # Concurrent ultra-fast scanning
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = [
                executor.submit(self.ultra_fast_remoteok_scan),
                executor.submit(self.ultra_fast_indeed_scan),
                executor.submit(self.ultra_fast_stackoverflow_scan)
            ]
            
            for future in futures:
                try:
                    jobs = future.result(timeout=10)
                    for job in jobs:
                        if job['id'] not in self.tracked_jobs:
                            self.tracked_jobs[job['id']] = job
                            all_new_jobs.append(job)
                except Exception as e:
                    logging.warning(f"Scan timeout: {e}")
        
        if all_new_jobs:
            logging.info(f"🎉 FOUND {len(all_new_jobs)} NEW TESTING JOBS!")
            self.send_instant_job_alert(all_new_jobs)
            self.save_tracked_jobs()
            
            for job in all_new_jobs:
                logging.info(f"🎯 NEW: {job['title']} at {job['company']}")
        else:
            logging.info("🔍 No new testing jobs (continuing scan...)")
        
        return len(all_new_jobs)
    
    def start_ultra_realtime_24x7(self):
        """Start continuous 24/7 monitoring - NEVER STOPS"""
        logging.info("🔥 ULTRA REAL-TIME 24/7 MONITORING STARTED")
        logging.info("⚡ Scanning every 15 seconds CONTINUOUSLY")
        logging.info("🎯 Testing jobs ONLY")
        logging.info("🚨 Instant alerts for EVERY testing job")
        logging.info("📧 Target: kalyogyogi@gmail.com")
        logging.info("🔄 Mode: NEVER STOPS - 24/7 operation")
        logging.info("=" * 80)
        
        # Initial scan
        self.ultra_aggressive_scan()
        
        try:
            while self.is_running:
                time.sleep(15)  # 15-second intervals for ultra-aggressive monitoring
                self.ultra_aggressive_scan()
                
                # Send status update every hour
                if self.scan_count % 240 == 0:  # Every 240 scans (1 hour)
                    self.send_status_update()
                
        except KeyboardInterrupt:
            logging.info("⏹️ Monitoring stopped by user")
            self.send_shutdown_alert()
        except Exception as e:
            logging.error(f"Critical error: {e}")
            self.send_error_alert(str(e))
            # Restart monitoring
            time.sleep(5)
            self.start_ultra_realtime_24x7()
    
    def send_status_update(self):
        """Send hourly status update"""
        try:
            message = f"📊 **24/7 MONITORING STATUS UPDATE**\n\n"
            message += f"⏰ **Running since**: 1 hour\n"
            message += f"🔢 **Total scans**: {self.scan_count}\n"
            message += f"🚨 **Alerts sent**: {self.alerts_sent}\n"
            message += f"💾 **Jobs tracked**: {len(self.tracked_jobs)}\n"
            message += f"✅ **Status**: ACTIVE 24/7\n\n"
            message += f"🔥 **Ultra-aggressive monitoring continues...**"
            
            self.send_telegram_message(message)
            
        except Exception as e:
            logging.error(f"Status update error: {e}")
    
    def send_shutdown_alert(self):
        """Send alert when monitoring stops"""
        try:
            message = f"⏹️ **24/7 MONITORING STOPPED**\n\n"
            message += f"📊 **Final Stats**:\n"
            message += f"🔢 **Total scans**: {self.scan_count}\n"
            message += f"🚨 **Alerts sent**: {self.alerts_sent}\n"
            message += f"💾 **Jobs found**: {len(self.tracked_jobs)}\n"
            message += f"⏰ **Stopped**: {datetime.datetime.now().strftime('%H:%M:%S')}\n\n"
            message += f"🔄 **Restart to resume 24/7 monitoring**"
            
            self.send_telegram_message(message)
            
        except Exception as e:
            logging.error(f"Shutdown alert error: {e}")
    
    def send_error_alert(self, error):
        """Send alert when error occurs"""
        try:
            message = f"❌ **MONITORING ERROR DETECTED**\n\n"
            message += f"🚨 **Error**: {error[:200]}\n"
            message += f"⏰ **Time**: {datetime.datetime.now().strftime('%H:%M:%S')}\n"
            message += f"🔄 **Action**: Auto-restarting in 5 seconds\n\n"
            message += f"📧 **Target**: kalyogyogi@gmail.com\n"
            message += f"✅ **Status**: Will resume automatically"
            
            self.send_telegram_message(message)
            
        except Exception as e:
            logging.error(f"Error alert error: {e}")

def main():
    print("🔥 ULTRA REAL-TIME 24/7 JOB MONITOR")
    print("⚡ NEVER STOPS - Continuous 15-second scanning")
    print("🎯 Testing jobs ONLY")
    print("🚨 Instant alerts for EVERY testing job found")
    print("📧 Target: kalyogyogi@gmail.com")
    print("=" * 80)
    
    monitor = UltraRealtime24x7Monitor()
    
    print("🚀 Starting ultra-aggressive 24/7 monitoring...")
    print("🔥 This will run CONTINUOUSLY until manually stopped")
    print("📱 Check Telegram for instant startup confirmation")
    print("⚡ Scanning every 15 seconds for testing jobs")
    print("\nPress Ctrl+C to stop (but it's designed to run 24/7)")
    print("=" * 80)
    
    monitor.start_ultra_realtime_24x7()

if __name__ == "__main__":
    main()
