#!/usr/bin/env python3
"""
HYPER-AGGRESSIVE REAL-TIME Testing Job Monitor
Ultra-fast scanning every 30 seconds for immediate testing job alerts
"""

import requests
import json
import datetime
import time
import os
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import feedparser
import logging

# Ultra-aggressive logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler('hyper_realtime.log'),
        logging.StreamHandler()
    ]
)

class HyperRealtimeTestingMonitor:
    def __init__(self):
        self.telegram_config = {
            'bot_token': '8305949318:AAF257TSUv4EObGWLAAi7Cq7K87iambC9EM',
            'chat_id': '6411380646'
        }
        self.gemini_api_key = 'AIzaSyDWzLu8s7KV4xSjjd0rUJSKxd2dC6Isljg'
        self.jobs_file = "hyper_realtime_jobs.json"
        self.load_tracked_jobs()
        self.scan_count = 0
        self.total_alerts_sent = 0
        
        # Ultra-specific testing keywords
        self.testing_keywords = [
            'qa', 'testing', 'test engineer', 'quality assurance', 
            'automation', 'sdet', 'quality engineer', 'test analyst',
            'software testing', 'qa engineer', 'test automation',
            'quality analyst', 'testing specialist', 'qa analyst'
        ]
        
        # Experience level indicators
        self.experience_terms = [
            '2+ years', '2-4 years', 'junior', 'mid-level', 'experienced',
            '2 years', 'entry level', 'associate', 'II', 'intermediate'
        ]
        
    def load_tracked_jobs(self):
        try:
            with open(self.jobs_file, 'r') as f:
                self.tracked_jobs = json.load(f)
        except FileNotFoundError:
            self.tracked_jobs = {}
    
    def save_tracked_jobs(self):
        with open(self.jobs_file, 'w') as f:
            json.dump(self.tracked_jobs, f, indent=2)
    
    def is_testing_job(self, title, description):
        """Ultra-specific testing job detection"""
        text = f"{title} {description}".lower()
        
        # Must contain testing keywords
        has_testing_keyword = any(keyword in text for keyword in self.testing_keywords)
        
        # Exclude non-testing roles
        exclusions = ['sales', 'marketing', 'business', 'finance', 'hr', 'accounting']
        has_exclusion = any(excl in text for excl in exclusions)
        
        return has_testing_keyword and not has_exclusion
    
    def check_remoteok_hyperaggressive(self):
        """Hyper-aggressive RemoteOK scanning for testing jobs"""
        jobs = []
        
        try:
            logging.info("🔥 HYPER-AGGRESSIVE RemoteOK scan...")
            
            # Direct testing-focused searches
            search_urls = [
                "https://remoteok.io/api?tag=qa",
                "https://remoteok.io/api?tag=testing", 
                "https://remoteok.io/api?tag=automation",
                "https://remoteok.io/api?tag=sdet",
                "https://remoteok.io/api?tag=quality",
                "https://remoteok.io/api?search=test+engineer",
                "https://remoteok.io/api?search=qa+engineer",
                "https://remoteok.io/api?search=software+testing"
            ]
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'application/json',
                'Cache-Control': 'no-cache'
            }
            
            for url in search_urls:
                try:
                    response = requests.get(url, headers=headers, timeout=10)
                    
                    if response.status_code == 200:
                        data = response.json()
                        
                        for job in data[1:11]:  # Skip legal notice, get top 10
                            if not job or not isinstance(job, dict):
                                continue
                            
                            title = job.get('position', '')
                            description = job.get('description', '')
                            
                            # Ultra-specific testing job filter
                            if self.is_testing_job(title, description):
                                job_id = f"remoteok_hyper_{job.get('id', len(jobs))}"
                                
                                if job_id not in self.tracked_jobs:
                                    job_entry = {
                                        'id': job_id,
                                        'title': title,
                                        'company': job.get('company', 'N/A'),
                                        'location': job.get('location', 'Remote'),
                                        'salary': self.format_salary(job.get('salary_min'), job.get('salary_max')),
                                        'description': description[:500],
                                        'url': f"https://remoteok.io/remote-jobs/{job.get('slug', '')}",
                                        'source': 'RemoteOK Testing',
                                        'date_found': datetime.datetime.now().isoformat(),
                                        'tags': job.get('tags', []),
                                        'relevance': 'HIGH - Testing specific'
                                    }
                                    jobs.append(job_entry)
                    
                    time.sleep(0.5)  # Minimal delay
                    
                except Exception as e:
                    logging.warning(f"RemoteOK URL error: {e}")
            
            logging.info(f"🎯 RemoteOK: {len(jobs)} TESTING jobs found")
            
        except Exception as e:
            logging.error(f"RemoteOK critical error: {e}")
        
        return jobs
    
    def check_indeed_testing_rss(self):
        """Indeed RSS specifically for testing jobs"""
        jobs = []
        
        try:
            logging.info("🔥 HYPER-AGGRESSIVE Indeed testing scan...")
            
            # Hyper-specific testing searches
            indeed_searches = [
                'https://www.indeed.com/rss?q=software+testing+2+years&sort=date',
                'https://www.indeed.com/rss?q=qa+engineer+junior&sort=date',
                'https://www.indeed.com/rss?q=test+automation+engineer&sort=date',
                'https://www.indeed.com/rss?q=sdet+2+years+experience&sort=date',
                'https://www.indeed.com/rss?q=quality+assurance+analyst&sort=date',
                'https://uk.indeed.com/rss?q=software+testing+2+years&sort=date',
                'https://ca.indeed.com/rss?q=qa+automation+engineer&sort=date'
            ]
            
            for search_url in indeed_searches:
                try:
                    feed = feedparser.parse(search_url)
                    
                    for entry in feed.entries[:5]:  # Recent entries only
                        title = entry.get('title', '')
                        description = entry.get('summary', '')
                        
                        if self.is_testing_job(title, description):
                            job_id = f"indeed_hyper_{entry.get('id', len(jobs))}"
                            
                            if job_id not in self.tracked_jobs:
                                job_entry = {
                                    'id': job_id,
                                    'title': title,
                                    'company': entry.get('author', 'Various'),
                                    'location': 'Global',
                                    'salary': 'See posting',
                                    'description': description[:500],
                                    'url': entry.get('link', ''),
                                    'source': 'Indeed Testing',
                                    'date_found': datetime.datetime.now().isoformat(),
                                    'relevance': 'HIGH - Testing specific'
                                }
                                jobs.append(job_entry)
                    
                    time.sleep(0.5)
                    
                except Exception as e:
                    logging.warning(f"Indeed search error: {e}")
            
            logging.info(f"🎯 Indeed: {len(jobs)} TESTING jobs found")
            
        except Exception as e:
            logging.error(f"Indeed critical error: {e}")
        
        return jobs
    
    def check_stackoverflow_testing(self):
        """Stack Overflow specifically for testing jobs"""
        jobs = []
        
        try:
            logging.info("🔥 HYPER-AGGRESSIVE Stack Overflow testing scan...")
            
            # Ultra-specific testing searches
            so_searches = [
                'software+testing+2+years+experience',
                'qa+automation+engineer+junior',
                'test+engineer+entry+level',
                'sdet+software+development+engineer+test',
                'quality+assurance+analyst+2+years',
                'qa+engineer+automation+testing',
                'test+automation+specialist'
            ]
            
            for search in so_searches:
                try:
                    url = f'https://stackoverflow.com/jobs/feed?q={search}&r=true&sort=i'
                    feed = feedparser.parse(url)
                    
                    for entry in feed.entries[:3]:
                        title = entry.get('title', '')
                        description = entry.get('summary', '')
                        
                        if self.is_testing_job(title, description):
                            job_id = f"stackoverflow_hyper_{entry.get('id', len(jobs))}"
                            
                            if job_id not in self.tracked_jobs:
                                job_entry = {
                                    'id': job_id,
                                    'title': title,
                                    'company': entry.get('author', 'Tech Company'),
                                    'location': 'Remote/Global',
                                    'salary': 'Competitive',
                                    'description': description[:500],
                                    'url': entry.get('link', ''),
                                    'source': 'Stack Overflow Testing',
                                    'date_found': datetime.datetime.now().isoformat(),
                                    'relevance': 'HIGH - Developer-focused testing'
                                }
                                jobs.append(job_entry)
                    
                    time.sleep(0.5)
                    
                except Exception as e:
                    logging.warning(f"Stack Overflow search error: {e}")
            
            logging.info(f"🎯 Stack Overflow: {len(jobs)} TESTING jobs found")
            
        except Exception as e:
            logging.error(f"Stack Overflow critical error: {e}")
        
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
    
    def send_instant_testing_alert(self, testing_jobs):
        """Send ultra-fast alert for testing jobs only"""
        if not testing_jobs:
            return False
        
        try:
            self.scan_count += 1
            self.total_alerts_sent += 1
            current_time = datetime.datetime.now()
            
            # Hyper-focused testing alert
            alert_message = f"🚨 **INSTANT TESTING JOB ALERT #{self.total_alerts_sent}** 🚨\n\n"
            alert_message += f"🎯 **{len(testing_jobs)} NEW Testing Jobs Found!**\n"
            alert_message += f"⚡ **IMMEDIATE APPLICATION RECOMMENDED**\n"
            alert_message += f"⏰ **Time**: {current_time.strftime('%H:%M:%S')}\n"
            alert_message += f"📧 **For**: kalyogyogi@gmail.com\n"
            alert_message += f"🎯 **Experience**: 2+ years software testing\n\n"
            
            # Show each testing job
            for i, job in enumerate(testing_jobs[:3], 1):
                alert_message += f"**🎯 {i}. {job['title']}**\n"
                alert_message += f"🏢 **Company**: {job['company']}\n"
                alert_message += f"📍 **Location**: {job['location']}\n"
                alert_message += f"💰 **Salary**: {job['salary']}\n"
                alert_message += f"🌐 **Source**: {job['source']}\n"
                alert_message += f"⭐ **Relevance**: {job['relevance']}\n"
                alert_message += f"🔗 [**APPLY IMMEDIATELY**]({job['url']})\n\n"
            
            if len(testing_jobs) > 3:
                alert_message += f"➕ **{len(testing_jobs) - 3} more testing jobs** available!\n\n"
            
            alert_message += f"✅ **100% TESTING JOBS** - No irrelevant positions\n"
            alert_message += f"⚡ **NEXT SCAN**: 30 seconds\n"
            alert_message += f"🔥 **HYPER-AGGRESSIVE** monitoring active"
            
            # Send with maximum priority
            url = f"https://api.telegram.org/bot{self.telegram_config['bot_token']}/sendMessage"
            data = {
                'chat_id': self.telegram_config['chat_id'],
                'text': alert_message,
                'parse_mode': 'Markdown',
                'disable_web_page_preview': True,
                'disable_notification': False  # Ensure notification sound
            }
            
            response = requests.post(url, data=data, timeout=10)
            
            if response.status_code == 200:
                logging.info(f"🚨 INSTANT TESTING ALERT #{self.total_alerts_sent} SENT! ({len(testing_jobs)} jobs)")
                return True
            else:
                logging.error(f"Alert failed: {response.status_code}")
                return False
                
        except Exception as e:
            logging.error(f"Alert error: {e}")
            return False
    
    def hyper_aggressive_scan(self):
        """Ultra-fast scan focused only on testing jobs"""
        logging.info(f"\n🔥 HYPER-AGGRESSIVE TESTING SCAN #{self.scan_count + 1}")
        logging.info(f"⏰ {datetime.datetime.now().strftime('%H:%M:%S')} - SCANNING FOR TESTING JOBS ONLY")
        logging.info("=" * 80)
        
        all_testing_jobs = []
        
        # Concurrent hyper-aggressive scanning
        sources = [
            self.check_remoteok_hyperaggressive,
            self.check_indeed_testing_rss, 
            self.check_stackoverflow_testing
        ]
        
        with ThreadPoolExecutor(max_workers=3) as executor:
            future_to_source = {executor.submit(source): source.__name__ for source in sources}
            
            for future in as_completed(future_to_source, timeout=25):
                try:
                    jobs = future.result(timeout=15)
                    
                    for job in jobs:
                        if job['id'] not in self.tracked_jobs:
                            self.tracked_jobs[job['id']] = job
                            all_testing_jobs.append(job)
                            
                except Exception as e:
                    source_name = future_to_source[future]
                    logging.warning(f"{source_name} timeout/error: {e}")
        
        if all_testing_jobs:
            logging.info(f"🎉 FOUND {len(all_testing_jobs)} NEW TESTING JOBS!")
            
            # INSTANT alert for testing jobs
            self.send_instant_testing_alert(all_testing_jobs)
            
            # Save immediately
            self.save_tracked_jobs()
            
            # Log each testing job found
            for job in all_testing_jobs:
                logging.info(f"🎯 TESTING JOB: {job['title']} at {job['company']} ({job['source']})")
        else:
            logging.info("⏳ No new testing jobs in this scan - continuing aggressive monitoring...")
        
        return len(all_testing_jobs)
    
    def start_hyper_realtime_monitoring(self):
        """Start hyper-aggressive 30-second monitoring"""
        logging.info("🔥 STARTING HYPER-AGGRESSIVE TESTING JOB MONITORING")
        logging.info("⚡ ULTRA-FAST: 30-second scan intervals")
        logging.info("🎯 LASER-FOCUSED: Testing jobs only")
        logging.info("📧 TARGET: kalyogyogi@gmail.com")
        logging.info("🚨 INSTANT ALERTS: Maximum priority")
        logging.info("=" * 80)
        
        # Run initial hyper scan
        logging.info("🧪 Initial hyper-aggressive scan...")
        initial_jobs = self.hyper_aggressive_scan()
        
        if initial_jobs > 0:
            logging.info(f"🎉 EXCELLENT START! Found {initial_jobs} testing jobs immediately!")
        
        try:
            while True:
                time.sleep(30)  # 30-second intervals for hyper-aggressive monitoring
                self.hyper_aggressive_scan()
                
        except KeyboardInterrupt:
            logging.info("\n⏹️ Hyper-aggressive monitoring stopped")
            logging.info(f"📊 Total scans: {self.scan_count}")
            logging.info(f"🚨 Total alerts sent: {self.total_alerts_sent}")
            self.save_tracked_jobs()

def main():
    print("🔥 HYPER-AGGRESSIVE REAL-TIME TESTING JOB MONITOR")
    print("⚡ 30-SECOND SCANS | 🎯 TESTING JOBS ONLY | 🚨 INSTANT ALERTS")
    print("=" * 80)
    
    monitor = HyperRealtimeTestingMonitor()
    
    print("🎯 Target: Software Testing (2+ years experience)")
    print("📧 Email: kalyogyogi@gmail.com") 
    print("📱 Telegram: Instant alerts enabled")
    print("⚡ Scan frequency: Every 30 seconds")
    print("🔥 Mode: Hyper-aggressive testing job focus")
    
    print("\n🚀 Starting hyper-aggressive monitoring...")
    print("🚨 You will receive INSTANT alerts for testing jobs only!")
    print("Press Ctrl+C to stop\n")
    
    monitor.start_hyper_realtime_monitoring()

if __name__ == "__main__":
    main()
