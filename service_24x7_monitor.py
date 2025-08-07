#!/usr/bin/env python3
"""
24/7 Windows Service Job Monitor
Runs as background service - TRUE 24/7 operation
"""

import requests
import json
import datetime
import time
import os
import threading
import logging
import sys
from concurrent.futures import ThreadPoolExecutor
import feedparser

# Service-level logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler('service_24x7.log'),
        logging.StreamHandler()
    ]
)

class Service24x7Monitor:
    def __init__(self):
        self.telegram_config = {
            'bot_token': '8305949318:AAF257TSUv4EObGWLAAi7Cq7K87iambC9EM',
            'chat_id': '6411380646'
        }
        self.jobs_file = "service_24x7_jobs.json"
        self.tracked_jobs = {}
        self.scan_count = 0
        self.alerts_sent = 0
        self.is_running = True
        self.load_tracked_jobs()
        
        # Send service start notification
        self.send_service_start_alert()
        
    def load_tracked_jobs(self):
        try:
            with open(self.jobs_file, 'r', encoding='utf-8') as f:
                self.tracked_jobs = json.load(f)
        except:
            self.tracked_jobs = {}
    
    def save_tracked_jobs(self):
        try:
            with open(self.jobs_file, 'w', encoding='utf-8') as f:
                json.dump(self.tracked_jobs, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logging.error(f"Save error: {e}")
    
    def send_service_start_alert(self):
        """Send alert when service starts"""
        try:
            message = f"🔥 **24/7 SERVICE MONITORING STARTED** 🔥\n\n"
            message += f"⏰ **Started**: {datetime.datetime.now().strftime('%H:%M:%S')}\n"
            message += f"📅 **Date**: {datetime.datetime.now().strftime('%Y-%m-%d')}\n"
            message += f"🎯 **Target**: kalyogyogi@gmail.com\n"
            message += f"⚡ **Scan Frequency**: Every 10 seconds\n"
            message += f"🔄 **Mode**: TRUE 24/7 service operation\n"
            message += f"🚨 **Alert Mode**: INSTANT for testing jobs\n\n"
            message += f"✅ **Service Status**: ACTIVE\n"
            message += f"🎯 **Job Focus**: QA, Testing, Automation, SDET only\n"
            message += f"📱 **Alerts**: Maximum priority notifications\n\n"
            message += f"🔥 **True 24/7 monitoring now active!**\n"
            message += f"⚡ **Ultra-fast 10-second scanning**"
            
            self.send_telegram_message(message)
            logging.info("🔥 Service start alert sent!")
            
        except Exception as e:
            logging.error(f"Service start alert error: {e}")
    
    def send_telegram_message(self, message):
        """Send Telegram message with enhanced retry"""
        for attempt in range(5):
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
                    return True
                else:
                    logging.warning(f"Telegram response: {response.status_code}")
                    
            except Exception as e:
                logging.warning(f"Telegram attempt {attempt + 1} failed: {e}")
                time.sleep(2)
        
        return False
    
    def lightning_fast_job_scan(self):
        """Lightning-fast job scanning"""
        all_jobs = []
        
        # Ultra-fast RemoteOK scan
        try:
            url = "https://remoteok.io/api?tag=qa"
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                data = response.json()
                
                for job in data[1:8]:  # Top 7 jobs
                    if not job or not isinstance(job, dict):
                        continue
                        
                    title = str(job.get('position', '')).lower()
                    
                    # Ultra-specific testing filter
                    testing_keywords = ['qa', 'test', 'quality', 'automation', 'sdet']
                    if any(keyword in title for keyword in testing_keywords):
                        job_id = f"service_remoteok_{job.get('id', len(all_jobs))}"
                        
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
                                'priority': 'HIGH'
                            }
                            all_jobs.append(job_entry)
        except:
            pass  # Continue scanning other sources
        
        # Ultra-fast Indeed scan
        try:
            feed_url = 'https://www.indeed.com/rss?q=qa+engineer&sort=date'
            feed = feedparser.parse(feed_url)
            
            for entry in feed.entries[:5]:  # Top 5
                title = str(entry.get('title', '')).lower()
                
                testing_keywords = ['qa', 'test', 'quality', 'automation', 'sdet']
                if any(keyword in title for keyword in testing_keywords):
                    job_id = f"service_indeed_{entry.get('id', len(all_jobs))}"
                    
                    if job_id not in self.tracked_jobs:
                        job_entry = {
                            'id': job_id,
                            'title': entry.get('title', 'Testing Position'),
                            'company': entry.get('author', 'Company'),
                            'location': 'Various',
                            'salary': 'See posting',
                            'url': entry.get('link', ''),
                            'source': 'Indeed',
                            'found_at': datetime.datetime.now().isoformat(),
                            'priority': 'HIGH'
                        }
                        all_jobs.append(job_entry)
        except:
            pass  # Continue scanning
        
        return all_jobs
    
    def send_lightning_alert(self, jobs):
        """Send lightning-fast alert"""
        if not jobs:
            return False
        
        try:
            self.alerts_sent += 1
            current_time = datetime.datetime.now()
            
            message = f"⚡ **LIGHTNING TESTING ALERT #{self.alerts_sent}** ⚡\n\n"
            message += f"🎯 **{len(jobs)} NEW Testing Jobs!**\n"
            message += f"🚨 **APPLY IMMEDIATELY**\n"
            message += f"⏰ **{current_time.strftime('%H:%M:%S')}**\n"
            message += f"📧 **kalyogyogi@gmail.com**\n\n"
            
            for i, job in enumerate(jobs[:2], 1):  # Show max 2 for speed
                message += f"**⚡ {i}. {job['title']}**\n"
                message += f"🏢 {job['company']}\n"
                message += f"💰 {job['salary']}\n"
                message += f"🔗 [**APPLY**]({job['url']})\n\n"
            
            if len(jobs) > 2:
                message += f"➕ **{len(jobs) - 2} more** testing jobs!\n\n"
            
            message += f"⚡ **Next scan**: 10 seconds\n"
            message += f"🔥 **24/7 service active**"
            
            if self.send_telegram_message(message):
                logging.info(f"⚡ LIGHTNING ALERT #{self.alerts_sent} sent! ({len(jobs)} jobs)")
                return True
            else:
                logging.error("Lightning alert failed")
                return False
                
        except Exception as e:
            logging.error(f"Lightning alert error: {e}")
            return False
    
    def service_scan_cycle(self):
        """Service scan cycle - ultra-fast"""
        self.scan_count += 1
        
        # Quick scan with minimal logging for performance
        new_jobs = self.lightning_fast_job_scan()
        
        if new_jobs:
            for job in new_jobs:
                self.tracked_jobs[job['id']] = job
            
            logging.info(f"⚡ SCAN #{self.scan_count}: {len(new_jobs)} NEW testing jobs!")
            self.send_lightning_alert(new_jobs)
            self.save_tracked_jobs()
        else:
            # Minimal logging to reduce overhead
            if self.scan_count % 360 == 0:  # Log every hour (360 scans * 10 seconds)
                logging.info(f"🔄 Service active - Scan #{self.scan_count} complete")
        
        return len(new_jobs)
    
    def run_24x7_service(self):
        """Run true 24/7 service"""
        logging.info("🔥 24/7 SERVICE MONITORING STARTED")
        logging.info("⚡ Lightning-fast 10-second scanning")
        logging.info("🎯 Testing jobs ONLY")
        logging.info("🔄 TRUE 24/7 operation - runs continuously")
        logging.info("📧 Target: kalyogyogi@gmail.com")
        logging.info("=" * 80)
        
        # Service loop - runs forever
        while self.is_running:
            try:
                self.service_scan_cycle()
                time.sleep(10)  # 10-second intervals for lightning-fast monitoring
                
                # Hourly status (every 360 scans)
                if self.scan_count % 360 == 0:
                    self.send_hourly_status()
                
                # Daily restart for memory cleanup (every 8640 scans = 24 hours)
                if self.scan_count % 8640 == 0:
                    logging.info("🔄 Daily restart for optimization...")
                    self.send_restart_notification()
                    break  # Will restart via service wrapper
                
            except KeyboardInterrupt:
                logging.info("⏹️ Service stopped by user")
                self.send_shutdown_alert()
                break
            except Exception as e:
                logging.error(f"Service error: {e}")
                # Auto-recovery
                time.sleep(5)
                continue
    
    def send_hourly_status(self):
        """Send hourly status update"""
        try:
            hours = self.scan_count // 360
            message = f"📊 **24/7 SERVICE - {hours}H ACTIVE**\n\n"
            message += f"🔢 **Scans**: {self.scan_count}\n"
            message += f"🚨 **Alerts**: {self.alerts_sent}\n"
            message += f"💾 **Jobs**: {len(self.tracked_jobs)}\n"
            message += f"⚡ **Speed**: 10s intervals\n"
            message += f"✅ **Status**: ACTIVE 24/7"
            
            self.send_telegram_message(message)
            
        except Exception as e:
            logging.error(f"Status error: {e}")
    
    def send_restart_notification(self):
        """Send restart notification"""
        try:
            message = f"🔄 **24/7 SERVICE RESTART**\n\n"
            message += f"📊 **24 hours completed**\n"
            message += f"🚨 **Alerts sent**: {self.alerts_sent}\n"
            message += f"💾 **Jobs found**: {len(self.tracked_jobs)}\n"
            message += f"⚡ **Restarting for optimization**\n"
            message += f"✅ **Will resume automatically**"
            
            self.send_telegram_message(message)
            
        except Exception as e:
            logging.error(f"Restart notification error: {e}")
    
    def send_shutdown_alert(self):
        """Send shutdown alert"""
        try:
            message = f"⏹️ **24/7 SERVICE STOPPED**\n\n"
            message += f"📊 **Runtime**: {self.scan_count * 10 // 3600} hours\n"
            message += f"🚨 **Total alerts**: {self.alerts_sent}\n"
            message += f"💾 **Jobs found**: {len(self.tracked_jobs)}\n"
            message += f"⏰ **Stopped**: {datetime.datetime.now().strftime('%H:%M:%S')}\n"
            message += f"🔄 **Restart to resume**"
            
            self.send_telegram_message(message)
            
        except Exception as e:
            logging.error(f"Shutdown alert error: {e}")

def main():
    """Main service entry point"""
    print("🔥 24/7 SERVICE MONITORING")
    print("⚡ Lightning-fast 10-second scanning")
    print("🎯 Testing jobs ONLY")
    print("🔄 TRUE 24/7 operation")
    print("📧 Target: kalyogyogi@gmail.com")
    print("=" * 60)
    
    # Auto-restart wrapper
    while True:
        try:
            monitor = Service24x7Monitor()
            print("🚀 Starting 24/7 service...")
            print("📱 Check Telegram for startup confirmation")
            print("⚡ Lightning-fast scanning every 10 seconds")
            print("🔄 Runs continuously until manually stopped")
            print("\nPress Ctrl+C to stop service")
            print("=" * 60)
            
            monitor.run_24x7_service()
            
            # If we reach here, it's a planned restart
            print("🔄 Service restarting for optimization...")
            time.sleep(5)
            
        except KeyboardInterrupt:
            print("\n⏹️ Service stopped by user")
            break
        except Exception as e:
            print(f"❌ Service error: {e}")
            print("🔄 Auto-restarting in 10 seconds...")
            time.sleep(10)

if __name__ == "__main__":
    main()
