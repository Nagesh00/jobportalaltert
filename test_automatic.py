#!/usr/bin/env python3
"""
Quick Test of Automatic Monitor
Tests the automatic system before starting 24/7 monitoring
"""

import requests
import datetime
import json

def test_automatic_system():
    print("🧪 TESTING AUTOMATIC MONITOR SYSTEM")
    print("=" * 50)
    print(f"⏰ Time: {datetime.datetime.now().strftime('%H:%M:%S')}")
    
    # Test configurations
    telegram_config = {
        'bot_token': '8305949318:AAF257TSUv4EObGWLAAi7Cq7K87iambC9EM',
        'chat_id': '6411380646'
    }
    
    reed_api_key = 'a3109410-807f-4753-b098-353adb07a966'
    jooble_api_key = '4452241a-50c6-416b-a47a-98261c93fd39'
    
    def test_telegram():
        """Test Telegram connectivity"""
        try:
            message = f"🧪 **AUTOMATIC SYSTEM TEST** 🧪\n\n"
            message += f"⏰ Test Time: {datetime.datetime.now().strftime('%H:%M:%S')}\n"
            message += f"✅ Testing automatic job monitor\n"
            message += f"🚀 If you see this, alerts will work!"
            
            url = f"https://api.telegram.org/bot{telegram_config['bot_token']}/sendMessage"
            data = {'chat_id': telegram_config['chat_id'], 'text': message, 'parse_mode': 'Markdown'}
            
            response = requests.post(url, data=data, timeout=10)
            return response.status_code == 200
        except:
            return False
    
    def test_job_sources():
        """Test job source connectivity"""
        sources_ok = 0
        
        # Test RemoteOK
        try:
            url = "https://remoteok.io/api"
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                sources_ok += 1
        except:
            pass
        
        # Test Jooble
        try:
            url = f"https://jooble.org/api/{jooble_api_key}"
            params = {'keywords': 'software testing', 'location': '', 'page': '1'}
            headers = {'Content-Type': 'application/json'}
            response = requests.post(url, json=params, headers=headers, timeout=10)
            if response.status_code == 200:
                sources_ok += 1
        except:
            pass
        
        # Test Reed
        try:
            url = "https://www.reed.co.uk/api/1.0/search"
            params = {'keywords': 'software testing', 'resultsToTake': 1}
            auth = (reed_api_key, '')
            response = requests.get(url, params=params, auth=auth, timeout=10)
            if response.status_code == 200:
                sources_ok += 1
        except:
            pass
        
        return sources_ok
    
    # Run tests
    print(f"\n🔧 RUNNING SYSTEM TESTS:")
    
    # Test Telegram
    telegram_ok = test_telegram()
    print(f"📱 Telegram: {'✅ WORKING' if telegram_ok else '❌ FAILED'}")
    
    # Test job sources
    sources_working = test_job_sources()
    print(f"🌐 Job Sources: {sources_working}/3 working")
    
    # Overall result
    print(f"\n📊 TEST RESULTS:")
    if telegram_ok and sources_working >= 2:
        print(f"🎉 SYSTEM READY FOR AUTOMATIC MONITORING!")
        print(f"✅ Telegram alerts working")
        print(f"✅ Job sources accessible")
        print(f"✅ Ready to start 24/7 automatic monitoring")
        
        print(f"\n🚀 TO START AUTOMATIC MONITORING:")
        print(f"   1. Double-click: START_AUTOMATIC_24X7.bat")
        print(f"   2. Or run: python automatic_24x7_monitor.py")
        
        print(f"\n🔄 FOR AUTOMATIC STARTUP ON BOOT:")
        print(f"   1. Right-click: SETUP_AUTOMATIC_STARTUP.bat")
        print(f"   2. Select 'Run as Administrator'")
        
        return True
    else:
        print(f"⚠️ SYSTEM ISSUES DETECTED:")
        if not telegram_ok:
            print(f"   • Telegram connection failed")
        if sources_working < 2:
            print(f"   • Job sources not accessible")
        print(f"   • Check internet connection")
        
        return False

if __name__ == "__main__":
    test_result = test_automatic_system()
    
    if test_result:
        print(f"\n" + "="*50)
        print(f"🎯 YOUR AUTOMATIC JOB MONITOR IS READY!")
        print(f"🚀 Start it now for instant job alerts!")
        print(f"="*50)
    else:
        print(f"\n" + "="*50)
        print(f"⚠️ Please fix the issues before starting")
        print(f"="*50)
