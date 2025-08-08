#!/usr/bin/env python3
"""
GitHub Actions Compatible Job Monitor
Single scan for real-time job alerts
"""

import requests
import json
import datetime
import time
import os
import logging
from concurrent.futures import ThreadPoolExecutor
import feedparser

# GitHub Actions logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

class GitHubJobMonitor:
    def __init__(self):
        self.telegram_config = {
            'bot_token': os.environ.get('TELEGRAM_BOT_TOKEN', '8305949318:AAF257TSUv4EObGWLAAi7Cq7K87iambC9EM'),
            'chat_id': os.environ.get('TELEGRAM_CHAT_ID', '6411380646')
        }
        self.gemini_api_key = os.environ.get('GEMINI_API_KEY')
        self.reed_api_key = os.environ.get('REED_API_KEY', 'a3109410-807f-4753-b098-353adb07a966')
        self.jobs_file = "github_monitor_jobs.json"
        self.tracked_jobs = {}
        self.load_tracked_jobs()
        
    def load_tracked_jobs(self):
        try:
            with open(self.jobs_file, 'r', encoding='utf-8') as f:
                self.tracked_jobs = json.load(f)
        except:
            self.tracked_jobs = {}
    
    def save_tracked_jobs(self):
        with open(self.jobs_file, 'w', encoding='utf-8') as f:
            json.dump(self.tracked_jobs, f, indent=2, ensure_ascii=False)
    
    def send_telegram_alert(self, jobs):
        """Send Telegram alert for new jobs"""
        try:
            message = f"🚨 **NEW TESTING JOBS ALERT!**\n\n"
            message += f"🎯 **{len(jobs)} New Software Testing Jobs Found!**\n"
            message += f"⏰ **Time**: {datetime.datetime.now().strftime('%H:%M:%S')}\n\n"
            
            for i, job in enumerate(jobs[:3], 1):  # Show first 3 jobs
                message += f"**{i}. {job['title']}**\n"
                message += f"🏢 Company: {job['company']}\n"
                message += f"📍 Location: {job['location']}\n"
                message += f"💰 Salary: {job['salary']}\n"
                message += f"🔗 Apply: {job['url']}\n\n"
            
            if len(jobs) > 3:
                message += f"*...and {len(jobs) - 3} more jobs!*\n\n"
            
            message += "🚀 **Apply NOW! First to apply gets the job!**"
            
            url = f"https://api.telegram.org/bot{self.telegram_config['bot_token']}/sendMessage"
            data = {
                'chat_id': self.telegram_config['chat_id'],
                'text': message,
                'parse_mode': 'Markdown'
            }
            
            response = requests.post(url, data=data, timeout=10)
            if response.status_code == 200:
                logging.info(f"✅ Telegram alert sent for {len(jobs)} jobs")
                return True
            else:
                logging.error(f"❌ Telegram alert failed: {response.status_code}")
                return False
                
        except Exception as e:
            logging.error(f"❌ Telegram error: {str(e)}")
            return False
    
    def scan_remoteok(self):
        """Scan RemoteOK for testing jobs"""
        try:
            url = "https://remoteok.io/api"
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code != 200:
                return []
            
            jobs_data = response.json()
            if not jobs_data:
                return []
            
            # Skip first element (metadata)
            jobs = jobs_data[1:] if isinstance(jobs_data, list) and len(jobs_data) > 1 else []
            
            new_jobs = []
            for job in jobs:
                if not isinstance(job, dict):
                    continue
                
                # Check for testing keywords and experience
                title = str(job.get('position', '')).lower()
                description = str(job.get('description', '')).lower()
                tags = [str(tag).lower() for tag in job.get('tags', [])]
                
                # Testing keywords
                testing_keywords = ['test', 'qa', 'quality assurance', 'automation', 'selenium', 'cypress']
                has_testing = any(keyword in title for keyword in testing_keywords) or \
                             any(keyword in description for keyword in testing_keywords) or \
                             any(keyword in ' '.join(tags) for keyword in testing_keywords)
                
                # Experience keywords for 2+ years
                exp_keywords = ['2+ year', '2 year', 'experienced', 'senior', '3+ year', '4+ year', '5+ year']
                has_experience = any(keyword in description for keyword in exp_keywords)
                
                if has_testing and has_experience:
                    job_id = str(job.get('id', ''))
                    if job_id and job_id not in self.tracked_jobs:
                        new_job = {
                            'id': job_id,
                            'title': job.get('position', 'Software Tester'),
                            'company': job.get('company', 'Remote Company'),
                            'location': job.get('location', 'Remote'),
                            'salary': job.get('salary_min', 'Competitive'),
                            'url': f"https://remoteok.io/remote-jobs/{job_id}",
                            'source': 'RemoteOK',
                            'posted': datetime.datetime.now().isoformat(),
                            'tags': tags
                        }
                        new_jobs.append(new_job)
                        self.tracked_jobs[job_id] = new_job
            
            return new_jobs
            
        except Exception as e:
            logging.error(f"❌ RemoteOK scan error: {str(e)}")
            return []
    
    def scan_stackoverflow(self):
        """Scan Stack Overflow Jobs RSS feed"""
        try:
            url = "https://stackoverflow.com/jobs/feed"
            feed = feedparser.parse(url)
            
            new_jobs = []
            for entry in feed.entries[:20]:  # Check latest 20 jobs
                title = entry.title.lower()
                summary = entry.summary.lower() if hasattr(entry, 'summary') else ''
                
                # Check for testing keywords
                testing_keywords = ['test', 'qa', 'quality', 'automation', 'selenium']
                if any(keyword in title or keyword in summary for keyword in testing_keywords):
                    job_id = f"so_{hash(entry.link)}"
                    
                    if job_id not in self.tracked_jobs:
                        new_job = {
                            'id': job_id,
                            'title': entry.title,
                            'company': 'Various Companies',
                            'location': 'Multiple Locations',
                            'salary': 'Competitive',
                            'url': entry.link,
                            'source': 'Stack Overflow',
                            'posted': datetime.datetime.now().isoformat()
                        }
                        new_jobs.append(new_job)
                        self.tracked_jobs[job_id] = new_job
            
            return new_jobs
            
        except Exception as e:
            logging.error(f"❌ Stack Overflow scan error: {str(e)}")
            return []
    
    def scan_indeed_rss(self):
        """Scan Indeed RSS feeds for testing jobs"""
        try:
            # Multiple Indeed RSS feeds for testing jobs
            feeds = [
                "https://rss.indeed.com/rss?q=software+testing&l=",
                "https://rss.indeed.com/rss?q=qa+automation&l=",
                "https://rss.indeed.com/rss?q=test+engineer&l="
            ]
            
            new_jobs = []
            for feed_url in feeds:
                try:
                    feed = feedparser.parse(feed_url)
                    for entry in feed.entries[:10]:  # Check latest 10 from each feed
                        title = entry.title.lower()
                        summary = entry.summary.lower() if hasattr(entry, 'summary') else ''
                        
                        # Check for experience level
                        exp_keywords = ['2+ year', '2 year', 'experienced', 'senior']
                        if any(keyword in summary for keyword in exp_keywords):
                            job_id = f"indeed_{hash(entry.link)}"
                            
                            if job_id not in self.tracked_jobs:
                                new_job = {
                                    'id': job_id,
                                    'title': entry.title,
                                    'company': 'Various Companies',
                                    'location': 'Multiple Locations',
                                    'salary': 'Competitive',
                                    'url': entry.link,
                                    'source': 'Indeed',
                                    'posted': datetime.datetime.now().isoformat()
                                }
                                new_jobs.append(new_job)
                                self.tracked_jobs[job_id] = new_job
                except:
                    continue
            
            return new_jobs
            
        except Exception as e:
            logging.error(f"❌ Indeed RSS scan error: {str(e)}")
            return []
    
    def scan_reed_uk(self):
        """Scan Reed.co.uk API for testing jobs"""
        try:
            # Reed.co.uk API endpoint
            base_url = "https://www.reed.co.uk/api/1.0/search"
            
            # Search parameters for testing jobs
            params = {
                'keywords': 'software testing OR qa automation OR test engineer',
                'locationName': '',  # All locations
                'distanceFromLocation': 50,
                'permanent': 'true',
                'resultsToTake': 20,
                'resultsToSkip': 0
            }
            
            # API authentication (Reed uses basic auth with API key as username)
            auth = (self.reed_api_key, '')
            headers = {'User-Agent': 'JobMonitor/1.0'}
            
            response = requests.get(base_url, params=params, auth=auth, headers=headers, timeout=15)
            
            if response.status_code != 200:
                logging.error(f"❌ Reed API failed: {response.status_code}")
                return []
            
            data = response.json()
            jobs_data = data.get('results', [])
            
            new_jobs = []
            for job in jobs_data:
                # Check for testing keywords and experience
                title = str(job.get('jobTitle', '')).lower()
                description = str(job.get('jobDescription', '')).lower()
                
                # Testing keywords
                testing_keywords = ['test', 'qa', 'quality assurance', 'automation', 'selenium', 'cypress']
                has_testing = any(keyword in title or keyword in description for keyword in testing_keywords)
                
                # Experience keywords for 2+ years
                exp_keywords = ['2+ year', '2 year', 'experienced', 'senior', '3+ year', '4+ year', '5+ year']
                has_experience = any(keyword in description for keyword in exp_keywords)
                
                if has_testing and has_experience:
                    job_id = f"reed_{job.get('jobId', '')}"
                    
                    if job_id not in self.tracked_jobs:
                        # Format salary
                        salary_min = job.get('minimumSalary', 0)
                        salary_max = job.get('maximumSalary', 0)
                        if salary_min and salary_max:
                            salary = f"£{salary_min:,} - £{salary_max:,}"
                        elif salary_min:
                            salary = f"£{salary_min:,}+"
                        else:
                            salary = "Competitive"
                        
                        new_job = {
                            'id': job_id,
                            'title': job.get('jobTitle', 'Software Tester'),
                            'company': job.get('employerName', 'Reed Company'),
                            'location': job.get('locationName', 'UK'),
                            'salary': salary,
                            'url': job.get('jobUrl', f"https://www.reed.co.uk/jobs/{job.get('jobId', '')}"),
                            'source': 'Reed.co.uk',
                            'posted': datetime.datetime.now().isoformat(),
                            'description': job.get('jobDescription', '')[:200] + '...'
                        }
                        new_jobs.append(new_job)
                        self.tracked_jobs[job_id] = new_job
            
            logging.info(f"✅ Reed.co.uk: Found {len(new_jobs)} new testing jobs")
            return new_jobs
            
        except Exception as e:
            logging.error(f"❌ Reed.co.uk scan error: {str(e)}")
            return []
    
    def run_single_scan(self):
        """Run a single comprehensive scan"""
        logging.info("🔍 Starting GitHub Actions job scan...")
        all_new_jobs = []
        
        # Scan all sources concurrently (including Reed.co.uk)
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = [
                executor.submit(self.scan_remoteok),
                executor.submit(self.scan_stackoverflow),
                executor.submit(self.scan_indeed_rss),
                executor.submit(self.scan_reed_uk)
            ]
            
            for future in futures:
                try:
                    jobs = future.result(timeout=30)
                    all_new_jobs.extend(jobs)
                except Exception as e:
                    logging.error(f"Scan error: {str(e)}")
        
        # Send alerts if new jobs found
        if all_new_jobs:
            logging.info(f"🎯 Found {len(all_new_jobs)} new testing jobs!")
            
            # Save tracked jobs
            self.save_tracked_jobs()
            
            # Send Telegram alert
            self.send_telegram_alert(all_new_jobs)
            
            # Log success
            logging.info(f"✅ GitHub Actions scan complete: {len(all_new_jobs)} jobs processed")
            
            return len(all_new_jobs)
        else:
            logging.info("ℹ️ No new testing jobs found in this scan")
            return 0

if __name__ == "__main__":
    try:
        monitor = GitHubJobMonitor()
        new_jobs = monitor.run_single_scan()
        
        print(f"\n🎯 GITHUB ACTIONS SCAN RESULTS:")
        print(f"📊 New jobs found: {new_jobs}")
        print(f"📱 Alert sent: {'YES' if new_jobs > 0 else 'NO'}")
        
        if new_jobs > 0:
            print(f"✅ SUCCESS! Found {new_jobs} new testing jobs!")
        else:
            print("ℹ️ No new jobs in this scan - monitoring continues...")
            
    except Exception as e:
        logging.error(f"❌ Monitor error: {str(e)}")
        print(f"❌ Error: {str(e)}")
