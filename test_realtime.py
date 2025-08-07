#!/usr/bin/env python3
"""
Test Real-Time Job Monitor - Single Scan
"""

import requests
import json
import datetime
import os

def test_real_time_scan():
    """Test a single real-time scan"""
    print("🚨 TESTING REAL-TIME JOB MONITOR")
    print("=" * 50)
    
    # Telegram config
    telegram_config = {
        'bot_token': os.environ.get('TELEGRAM_BOT_TOKEN', '8305949318:AAF257TSUv4EObGWLAAi7Cq7K87iambC9EM'),
        'chat_id': os.environ.get('TELEGRAM_CHAT_ID', '6411380646')
    }
    
    def check_remoteok():
        """Check RemoteOK for latest jobs"""
        jobs = []
        try:
            print("🔍 Checking RemoteOK API for REAL JOBS...")
            
            url = "https://remoteok.io/api"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code == 200:
                data = response.json()
                
                testing_keywords = [
                    'test', 'testing', 'qa', 'quality assurance', 'automation',
                    'selenium', 'cypress', 'junit', 'pytest', 'tester', 'sdet'
                ]
                
                for job in data[1:20]:  # Check first 20 jobs
                    position = job.get('position', '').lower()
                    description = job.get('description', '').lower()
                    
                    # Check if it's a testing job
                    is_testing = any(keyword in position or keyword in description for keyword in testing_keywords)
                    
                    if is_testing:
                        job_data = {
                            'id': f"remoteok_{job.get('id', '')}",
                            'title': job.get('position', 'N/A'),
                            'company': job.get('company', 'N/A'),
                            'location': 'Remote',
                            'snippet': job.get('description', 'N/A')[:200],
                            'url': f"https://remoteok.io/remote-jobs/{job.get('id', '')}",
                            'source': 'RemoteOK',
                            'date_found': datetime.datetime.now().isoformat()
                        }
                        jobs.append(job_data)
                
                print(f"✅ Found {len(jobs)} REAL testing jobs on RemoteOK!")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        
        return jobs
    
    def send_telegram_alert(jobs):
        """Send real-time Telegram alert"""
        if not jobs:
            return
            
        try:
            alert_message = f"🚨 **REAL-TIME TEST ALERT** 🚨\n\n"
            alert_message += f"🎯 Found {len(jobs)} REAL Testing Jobs!\n"
            alert_message += f"⏰ Scanned at: {datetime.datetime.now().strftime('%H:%M:%S')}\n\n"
            
            for i, job in enumerate(jobs[:3], 1):
                alert_message += f"**{i}. {job['title']}**\n"
                alert_message += f"🏢 {job['company']}\n"
                alert_message += f"📍 {job['location']}\n"
                alert_message += f"🔗 [Apply Now]({job['url']})\n\n"
            
            if len(jobs) > 3:
                alert_message += f"+ {len(jobs) - 3} more jobs found!\n"
            
            alert_message += "✅ This is a REAL job alert - No demos!"
            
            # Send to Telegram
            telegram_url = f"https://api.telegram.org/bot{telegram_config['bot_token']}/sendMessage"
            data = {
                'chat_id': telegram_config['chat_id'],
                'text': alert_message,
                'parse_mode': 'Markdown',
                'disable_web_page_preview': False
            }
            
            response = requests.post(telegram_url, data=data, timeout=10)
            
            if response.status_code == 200:
                print(f"📱 REAL-TIME alert sent with {len(jobs)} jobs!")
                return True
            else:
                print(f"❌ Alert failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error sending alert: {str(e)}")
            return False
    
    # Run the test
    print("🔄 Scanning for REAL jobs...")
    real_jobs = check_remoteok()
    
    if real_jobs:
        print(f"\n🎉 SUCCESS! Found {len(real_jobs)} REAL testing jobs:")
        for job in real_jobs:
            print(f"  • {job['title']} at {job['company']}")
        
        print(f"\n📱 Sending Telegram alert...")
        if send_telegram_alert(real_jobs):
            print("✅ Real-time alert system working!")
        else:
            print("❌ Alert sending failed")
    else:
        print("ℹ️ No new testing jobs found in this scan")
    
    print(f"\n💡 This scan found REAL jobs from RemoteOK API")
    print("🚀 For continuous monitoring, use the full real-time monitor")

if __name__ == "__main__":
    test_real_time_scan()
