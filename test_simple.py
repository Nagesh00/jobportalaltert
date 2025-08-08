#!/usr/bin/env python3
"""
Simple Working Job Monitor Test
No complex imports - direct implementation
"""

import requests
import json
import datetime
import os

def test_simple_monitor():
    print("🧪 TESTING SIMPLE JOB MONITOR")
    print("=" * 50)
    
    # Configuration
    telegram_config = {
        'bot_token': '8305949318:AAF257TSUv4EObGWLAAi7Cq7K87iambC9EM',
        'chat_id': '6411380646'
    }
    
    print("📱 Telegram: CONFIGURED")
    print(f"⏰ Time: {datetime.datetime.now().strftime('%H:%M:%S')}")
    
    def send_telegram_test():
        """Send a test Telegram message"""
        try:
            message = f"🧪 **TEST ALERT** 🧪\n\n"
            message += f"⏰ Time: {datetime.datetime.now().strftime('%H:%M:%S')}\n"
            message += f"🚀 Job monitor is working!\n"
            message += f"📍 Ready for real-time job alerts!"
            
            url = f"https://api.telegram.org/bot{telegram_config['bot_token']}/sendMessage"
            data = {
                'chat_id': telegram_config['chat_id'],
                'text': message,
                'parse_mode': 'Markdown'
            }
            
            response = requests.post(url, data=data, timeout=10)
            if response.status_code == 200:
                print("✅ Telegram test message sent successfully!")
                return True
            else:
                print(f"❌ Telegram test failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Telegram error: {str(e)}")
            return False
    
    def test_remoteok():
        """Test RemoteOK API access"""
        try:
            print("\n🔍 Testing RemoteOK API...")
            url = "https://remoteok.io/api"
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code == 200:
                jobs_data = response.json()
                job_count = len(jobs_data) - 1 if isinstance(jobs_data, list) and len(jobs_data) > 1 else 0
                print(f"✅ RemoteOK API working! Found {job_count} total jobs")
                
                # Check for testing jobs
                testing_jobs = 0
                if isinstance(jobs_data, list) and len(jobs_data) > 1:
                    for job in jobs_data[1:20]:  # Check first 20 jobs
                        if isinstance(job, dict):
                            title = str(job.get('position', '')).lower()
                            description = str(job.get('description', '')).lower()
                            
                            testing_keywords = ['test', 'qa', 'quality assurance', 'automation']
                            if any(keyword in title or keyword in description for keyword in testing_keywords):
                                testing_jobs += 1
                
                print(f"🎯 Found {testing_jobs} testing-related jobs in sample")
                return True
            else:
                print(f"❌ RemoteOK API failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ RemoteOK error: {str(e)}")
            return False
    
    # Run tests
    print("\n🔧 RUNNING CONNECTIVITY TESTS:")
    
    # Test 1: Telegram
    telegram_ok = send_telegram_test()
    
    # Test 2: RemoteOK API
    remoteok_ok = test_remoteok()
    
    print(f"\n📊 TEST RESULTS:")
    print(f"📱 Telegram: {'✅ WORKING' if telegram_ok else '❌ FAILED'}")
    print(f"🌐 RemoteOK API: {'✅ WORKING' if remoteok_ok else '❌ FAILED'}")
    
    if telegram_ok and remoteok_ok:
        print(f"\n🎉 ALL TESTS PASSED!")
        print(f"✅ Your job monitor is ready to work!")
        print(f"\n🚀 Next steps:")
        print(f"   1. GitHub Actions should now work correctly")
        print(f"   2. Check your Telegram for the test message")
        print(f"   3. Monitor will find jobs automatically")
        
        return True
    else:
        print(f"\n⚠️ SOME TESTS FAILED!")
        if not telegram_ok:
            print(f"   • Check Telegram bot token and chat ID")
        if not remoteok_ok:
            print(f"   • Check internet connection")
        
        return False

if __name__ == "__main__":
    test_simple_monitor()
