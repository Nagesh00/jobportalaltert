#!/usr/bin/env python3
"""
ULTRA-AGGRESSIVE TRUE REAL-TIME 24/7 Job Monitor
Continuous scanning with 15-second intervals and instant alerts
"""

import requests
import json
import datetime
import time
import os
import threading
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor
import feedparser
import logging
import sys

# Ultra-aggressive logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - 🔥 %(message)s',
    handlers=[
        logging.FileHandler('true_realtime_24x7.log'),
        logging.StreamHandler()
    ]
)

class TrueRealtime24x7Monitor:
    def __init__(self):
        self.telegram_config = {
            'bot_token': '8305949318:AAF257TSUv4EObGWLAAi7Cq7K87iambC9EM',
            'chat_id': '6411380646'
        }
        self.jobs_file = "true_realtime_jobs.json"
        self.load_tracked_jobs()
        self.scan_count = 0
        self.alerts_sent = 0
        self.jobs_found_today = 0
        self.is_running = True
        
        # Ultra-specific testing patterns
        self.testing_patterns = [
            'qa engineer', 'test engineer', 'testing engineer', 'quality engineer',
            'qa analyst', 'test analyst', 'quality analyst', 'testing analyst',
            'qa automation', 'test automation', 'automation engineer', 'automation tester',
            'sdet', 'qa lead', 'test lead', 'quality lead', 'testing lead',
            'qa manager', 'test manager', 'quality manager', 'testing manager',
            'software tester', 'manual tester', 'automated tester', 'performance tester',
            'qa specialist', 'test specialist', 'quality specialist', 'testing specialist'
        ]
        
        # Send startup notification
        self.send_startup_notification()
        
    def send_startup_notification(self):
        """Send notification that monitoring has started"""
        try:
            message = f"🚀 **TRUE REAL-TIME 24/7 MONITORING STARTED**\n\n"
            message += f"⏰ **Started**: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            message += f"⚡ **Scan Interval**: 15 seconds\n"
            message += f"🎯 **Target**: Software Testing Jobs (2+ years)\n"
            message += f"📧 **For**: kalyogyogi@gmail.com\n"
            message += f"🔥 **Mode**: ULTRA-AGGRESSIVE\n\n"
            message += f"✅ **System is now actively scanning...**\n"
            message += f"🚨 **You will receive INSTANT alerts for every testing job!**"
            
            self.send_telegram_alert(message)
            logging.info("🚀 Startup notification sent!")
        except Exception as e:
            logging.error(f"Startup notification error: {e}")
    
    def load_tracked_jobs(self):
        try:
            with open(self.jobs_file, 'r') as f:
                self.tracked_jobs = json.load(f)
        except FileNotFoundError:
            self.tracked_jobs = {}
    
    def save_tracked_jobs(self):
        try:
            with open(self.jobs_file, 'w') as f:
                json.dump(self.tracked_jobs, f, indent=2)
        except Exception as e:
            logging.error(f"Save error: {e}")
    
    def is_testing_job(self, title, description):
        """Ultra-precise testing job detection"""
        text = f"{title} {description}".lower()
        
        # Must match testing patterns
        is_testing = any(pattern in text for pattern in self.testing_patterns)
        
        # Additional testing indicators
        testing_keywords = ['qa', 'test', 'quality', 'automation', 'sdet']
        has_keyword = any(keyword in text for keyword in testing_keywords)
        
        # Exclude non-testing roles
        exclusions = ['sales', 'marketing', 'business development', 'account', 'finance', 'hr', 'customer support']
        has_exclusion = any(excl in text for excl in exclusions)
        
        return (is_testing or has_keyword) and not has_exclusion
    
    def ultra_fast_remoteok_scan(self):
        """Ultra-fast RemoteOK scanning"""
        jobs = []
        try:
            # Multiple rapid API calls
            api_urls = [
                "https://remoteok.io/api?tag=qa",
                "https://remoteok.io/api?tag=testing",
                "https://remoteok.io/api?tag=automation",
                "https://remoteok.io/api?tag=sdet"
            ]
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'application/json'
            }
            
            for url in api_urls:
                try:
                    response = requests.get(url, headers=headers, timeout=8)
                    if response.status_code == 200:
                        data = response.json()
                        
                        for job in data[1:8]:  # Skip legal notice
                            if not job or not isinstance(job, dict):
                                continue
                            
                            title = job.get('position', '')
                            description = job.get('description', '')
                            
                            if self.is_testing_job(title, description):
                                job_id = f"remoteok_ultra_{job.get('id', len(jobs))}"
                                
                                if job_id not in self.tracked_jobs:
                                    job_entry = {
                                        'id': job_id,
                                        'title': title,
                                        'company': job.get('company', 'N/A'),
                                        'location': job.get('location', 'Remote'),
                                        'salary': self.format_salary(job.get('salary_min'), job.get('salary_max')),
                                        'url': f"https://remoteok.io/remote-jobs/{job.get('slug', '')}",
                                        'source': 'RemoteOK Ultra',
                                        'found_at': datetime.datetime.now().isoformat(),
                                        'urgency': 'HIGH'
                                    }
                                    jobs.append(job_entry)
                    
                    time.sleep(0.2)  # Minimal delay
                except Exception as e:
                    logging.warning(f"RemoteOK URL error: {e}")
            
        except Exception as e:
            logging.error(f"RemoteOK scan error: {e}")
        
        return jobs
    
    def ultra_fast_indeed_scan(self):
        """Ultra-fast Indeed RSS scanning"""
        jobs = []
        try:
            # Rapid RSS feeds
            feeds = [
                'https://www.indeed.com/rss?q=qa+engineer+2+years&sort=date&limit=10',
                'https://www.indeed.com/rss?q=test+engineer+junior&sort=date&limit=10',
                'https://www.indeed.com/rss?q=software+testing&sort=date&limit=10',
                'https://www.indeed.com/rss?q=qa+automation&sort=date&limit=10'
            ]
            
            for feed_url in feeds:
                try:
                    feed = feedparser.parse(feed_url)
                    
                    for entry in feed.entries[:5]:
                        title = entry.get('title', '')
                        description = entry.get('summary', '')
                        
                        if self.is_testing_job(title, description):
                            job_id = f"indeed_ultra_{entry.get('id', len(jobs))}"
                            
                            if job_id not in self.tracked_jobs:
                                job_entry = {
                                    'id': job_id,
                                    'title': title,
                                    'company': entry.get('author', 'Company'),
                                    'location': 'Various',
                                    'salary': 'Competitive',
                                    'url': entry.get('link', ''),
                                    'source': 'Indeed Ultra',
                                    'found_at': datetime.datetime.now().isoformat(),
                                    'urgency': 'HIGH'
                                }
                                jobs.append(job_entry)
                    
                    time.sleep(0.2)
                except Exception as e:
                    logging.warning(f"Indeed feed error: {e}")
                    
        except Exception as e:
            logging.error(f"Indeed scan error: {e}")
        
        return jobs
    
    def ultra_fast_stackoverflow_scan(self):
        """Ultra-fast Stack Overflow scanning"""
        jobs = []
        try:
            # Targeted searches
            searches = [
                'qa+engineer+2+years',
                'test+automation+engineer',
                'software+testing+junior',
                'sdet+engineer'
            ]
            
            for search in searches:
                try:
                    url = f'https://stackoverflow.com/jobs/feed?q={search}&sort=i&r=true'
                    feed = feedparser.parse(url)
                    
                    for entry in feed.entries[:3]:
                        title = entry.get('title', '')
                        description = entry.get('summary', '')
                        
                        if self.is_testing_job(title, description):
                            job_id = f"stackoverflow_ultra_{entry.get('id', len(jobs))}"
                            
                            if job_id not in self.tracked_jobs:
                                job_entry = {
                                    'id': job_id,
                                    'title': title,
                                    'company': entry.get('author', 'Tech Company'),
                                    'location': 'Remote',
                                    'salary': 'Competitive',
                                    'url': entry.get('link', ''),
                                    'source': 'Stack Overflow Ultra',
                                    'found_at': datetime.datetime.now().isoformat(),
                                    'urgency': 'HIGH'
                                }
                                jobs.append(job_entry)
                    
                    time.sleep(0.2)
                except Exception as e:
                    logging.warning(f"SO search error: {e}")
                    
        except Exception as e:
            logging.error(f"Stack Overflow scan error: {e}")
        
        return jobs
    
    def format_salary(self, min_sal, max_sal):
        try:
            if min_sal and max_sal:
                return f"${min_sal:,} - ${max_sal:,}"
            elif min_sal:
                return f"${min_sal:,}+"
            else:
                return "Competitive"
        except:
            return "Competitive"
    
    def send_telegram_alert(self, message):
        """Send Telegram alert with retry"""
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
    
    def send_instant_job_alert(self, new_jobs):
        """Send instant alert for new testing jobs"""
        if not new_jobs:
            return
        
        try:
            self.alerts_sent += 1
            self.jobs_found_today += len(new_jobs)
            current_time = datetime.datetime.now()
            
            message = f"🚨 **INSTANT TESTING JOB ALERT #{self.alerts_sent}** 🚨\n\n"
            message += f"🎯 **{len(new_jobs)} NEW Testing Jobs Found!**\n"
            message += f"⚡ **Time**: {current_time.strftime('%H:%M:%S')}\n"
            message += f"📅 **Date**: {current_time.strftime('%Y-%m-%d')}\n"
            message += f"🔥 **Scan #{self.scan_count}** - Ultra-aggressive mode\n"
            message += f"📧 **Target**: kalyogyogi@gmail.com\n\n"
            
            for i, job in enumerate(new_jobs[:2], 1):  # Show top 2
                message += f"**🎯 {i}. {job['title']}**\n"
                message += f"🏢 **Company**: {job['company']}\n"
                message += f"📍 **Location**: {job['location']}\n"
                message += f"💰 **Salary**: {job['salary']}\n"
                message += f"🌐 **Source**: {job['source']}\n"
                message += f"🚨 **Urgency**: {job['urgency']}\n"
                message += f"🔗 [**APPLY IMMEDIATELY**]({job['url']})\n\n"
            
            if len(new_jobs) > 2:
                message += f"➕ **{len(new_jobs) - 2} more testing jobs** found!\n\n"
            
            message += f"📊 **Today's Stats**:\n"
            message += f"🎯 Jobs found today: {self.jobs_found_today}\n"
            message += f"🚨 Alerts sent: {self.alerts_sent}\n"
            message += f"🔄 Total scans: {self.scan_count}\n\n"
            message += f"⚡ **Next scan in 15 seconds**\n"
            message += f"🔥 **TRUE REAL-TIME monitoring active**"
            
            if self.send_telegram_alert(message):
                logging.info(f"🚨 INSTANT ALERT #{self.alerts_sent} SENT! ({len(new_jobs)} testing jobs)")
            else:
                logging.error(f"❌ Alert #{self.alerts_sent} failed")
                
        except Exception as e:
            logging.error(f"Alert creation error: {e}")
    
    def ultra_aggressive_scan(self):
        """Ultra-aggressive 15-second scanning"""
        self.scan_count += 1
        current_time = datetime.datetime.now()
        
        logging.info(f"🔥 ULTRA SCAN #{self.scan_count} - {current_time.strftime('%H:%M:%S')}")
        
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
                    jobs = future.result(timeout=12)
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
                logging.info(f"🎯 NEW: {job['title']} at {job['company']} ({job['source']})")
        else:
            logging.info(f"⏳ Scan #{self.scan_count} complete - monitoring continues...")
        
        return len(all_new_jobs)
    
    def heartbeat_monitoring(self):
        """Send periodic heartbeat to confirm system is running"""
        while self.is_running:
            try:
                time.sleep(300)  # Every 5 minutes
                if self.is_running:
                    heartbeat_msg = f"💓 **SYSTEM HEARTBEAT**\n\n"
                    heartbeat_msg += f"⏰ **Time**: {datetime.datetime.now().strftime('%H:%M:%S')}\n"
                    heartbeat_msg += f"🔥 **Status**: ACTIVELY SCANNING\n"
                    heartbeat_msg += f"🔄 **Scans completed**: {self.scan_count}\n"
                    heartbeat_msg += f"🎯 **Jobs found today**: {self.jobs_found_today}\n"
                    heartbeat_msg += f"🚨 **Alerts sent**: {self.alerts_sent}\n"
                    heartbeat_msg += f"✅ **TRUE REAL-TIME monitoring is running**"
                    
                    self.send_telegram_alert(heartbeat_msg)
                    logging.info("💓 Heartbeat sent - system is alive")
            except Exception as e:
                logging.error(f"Heartbeat error: {e}")
    
    def start_true_realtime_24x7(self):
        """Start true real-time 24/7 monitoring"""
        logging.info("🔥 STARTING TRUE REAL-TIME 24/7 MONITORING")
        logging.info("⚡ ULTRA-AGGRESSIVE: 15-second scans")
        logging.info("🎯 TESTING JOBS ONLY")
        logging.info("🚨 INSTANT ALERTS")
        logging.info("💓 HEARTBEAT MONITORING")
        logging.info("🔄 CONTINUOUS 24/7 OPERATION")
        logging.info("=" * 80)
        
        # Start heartbeat monitoring in background
        heartbeat_thread = threading.Thread(target=self.heartbeat_monitoring, daemon=True)
        heartbeat_thread.start()
        
        # Initial scan
        self.ultra_aggressive_scan()
        
        try:
            while self.is_running:
                time.sleep(15)  # 15-second intervals
                self.ultra_aggressive_scan()
                
        except KeyboardInterrupt:
            self.is_running = False
            logging.info("\n⏹️ TRUE REAL-TIME monitoring stopped")
            
            # Send shutdown notification
            shutdown_msg = f"⏹️ **MONITORING STOPPED**\n\n"
            shutdown_msg += f"⏰ **Stopped**: {datetime.datetime.now().strftime('%H:%M:%S')}\n"
            shutdown_msg += f"📊 **Final Stats**:\n"
            shutdown_msg += f"🔄 Total scans: {self.scan_count}\n"
            shutdown_msg += f"🎯 Jobs found: {self.jobs_found_today}\n"
            shutdown_msg += f"🚨 Alerts sent: {self.alerts_sent}"
            
            self.send_telegram_alert(shutdown_msg)
            self.save_tracked_jobs()

def main():
    print("🔥 TRUE REAL-TIME 24/7 TESTING JOB MONITOR")
    print("⚡ 15-SECOND SCANS | 🎯 TESTING ONLY | 🚨 INSTANT ALERTS")
    print("💓 HEARTBEAT MONITORING | 🔄 CONTINUOUS 24/7")
    print("=" * 80)
    
    monitor = TrueRealtime24x7Monitor()
    
    print("🎯 Target: Software Testing (2+ years)")
    print("📧 Email: kalyogyogi@gmail.com")
    print("📱 Telegram: Ultra-priority alerts")
    print("⚡ Scan: Every 15 seconds")
    print("💓 Heartbeat: Every 5 minutes")
    print("🔥 Mode: TRUE REAL-TIME")
    
    print("\n🚀 Starting TRUE real-time monitoring...")
    print("🚨 INSTANT alerts for every testing job!")
    print("💓 Heartbeat confirms system is alive")
    print("Press Ctrl+C to stop\n")
    
    monitor.start_true_realtime_24x7()

if __name__ == "__main__":
    main()
