#!/usr/bin/env python3
"""
INSTANT JOB MONITOR TEST
Works immediately without complex setup
"""

import requests
import json
import datetime

def instant_test():
    print("🧪 INSTANT JOB MONITOR TEST")
    print("=" * 40)
    print(f"⏰ Time: {datetime.datetime.now()}")
    
    # Test Telegram
    def test_telegram():
        try:
            bot_token = '8305949318:AAF257TSUv4EObGWLAAi7Cq7K87iambC9EM'
            chat_id = '6411380646'
            
            message = f"🧪 INSTANT TEST\n⏰ {datetime.datetime.now().strftime('%H:%M:%S')}\n✅ Monitor is working!"
            
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            data = {'chat_id': chat_id, 'text': message}
            
            response = requests.post(url, data=data, timeout=10)
            return response.status_code == 200
        except:
            return False
    
    # Test Job API
    def test_jobs():
        try:
            url = "https://remoteok.io/api"
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                jobs = response.json()
                return len(jobs) > 1
            return False
        except:
            return False
    
    # Run tests
    telegram_ok = test_telegram()
    jobs_ok = test_jobs()
    
    print(f"\n📊 RESULTS:")
    print(f"📱 Telegram: {'✅' if telegram_ok else '❌'}")
    print(f"🌐 Job API: {'✅' if jobs_ok else '❌'}")
    
    if telegram_ok and jobs_ok:
        print(f"\n🎉 ALL WORKING!")
        print(f"✅ GitHub Actions should work now")
        print(f"✅ Check your Telegram for test message")
    else:
        print(f"\n⚠️ Issues detected:")
        if not telegram_ok:
            print(f"   - Telegram connection failed")
        if not jobs_ok:
            print(f"   - Job API connection failed")
    
    return telegram_ok and jobs_ok

if __name__ == "__main__":
    try:
        instant_test()
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Please check your internet connection")
