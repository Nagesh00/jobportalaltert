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
    
    # Test Job APIs (including Reed and Jooble)
    def test_jobs():
        try:
            # Test RemoteOK
            url = "https://remoteok.io/api"
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers, timeout=10)
            
            remoteok_ok = response.status_code == 200 and len(response.json()) > 1
            
            # Test Reed.co.uk
            reed_api_key = 'a3109410-807f-4753-b098-353adb07a966'
            reed_url = "https://www.reed.co.uk/api/1.0/search"
            reed_params = {'keywords': 'software testing', 'resultsToTake': 1}
            reed_auth = (reed_api_key, '')
            
            reed_response = requests.get(reed_url, params=reed_params, auth=reed_auth, timeout=10)
            reed_ok = reed_response.status_code == 200
            
            # Test Jooble
            jooble_api_key = '4452241a-50c6-416b-a47a-98261c93fd39'
            jooble_url = f"https://jooble.org/api/{jooble_api_key}"
            jooble_params = {'keywords': 'software testing', 'location': '', 'page': '1'}
            jooble_headers = {'Content-Type': 'application/json'}
            
            jooble_response = requests.post(jooble_url, json=jooble_params, headers=jooble_headers, timeout=10)
            jooble_ok = jooble_response.status_code == 200
            
            return remoteok_ok and reed_ok and jooble_ok
        except:
            return False
    
    # Run tests
    telegram_ok = test_telegram()
    jobs_ok = test_jobs()
    
    print(f"\n📊 RESULTS:")
    print(f"📱 Telegram: {'✅' if telegram_ok else '❌'}")
    print(f"🌐 Job APIs (RemoteOK + Reed + Jooble): {'✅' if jobs_ok else '❌'}")
    
    if telegram_ok and jobs_ok:
        print(f"\n🎉 ALL WORKING!")
        print(f"✅ GitHub Actions should work now")
        print(f"✅ Check your Telegram for test message")
        print(f"🇬🇧 Reed.co.uk API integrated!")
        print(f"🌍 Jooble API integrated!")
        print(f"📈 Now monitoring 5 job sources!")
    else:
        print(f"\n⚠️ Issues detected:")
        if not telegram_ok:
            print(f"   - Telegram connection failed")
        if not jobs_ok:
            print(f"   - Job API connections failed")
    
    return telegram_ok and jobs_ok

if __name__ == "__main__":
    try:
        instant_test()
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Please check your internet connection")
