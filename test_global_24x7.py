#!/usr/bin/env python3
"""
Quick test of the Global 24/7 Real-Time Job Monitor
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from global_24x7_realtime_monitor import Global24x7JobMonitor
import datetime

def test_global_monitor():
    print("🧪 TESTING GLOBAL 24/7 MONITOR")
    print("=" * 50)
    
    # Configuration
    email_config = {
        'sender_email': 'kalyogyogi@gmail.com',
        'app_password': os.environ.get('EMAIL_APP_PASSWORD'),
        'recipient_email': 'kalyogyogi@gmail.com'
    }
    
    telegram_config = {
        'bot_token': '8305949318:AAF257TSUv4EObGWLAAi7Cq7K87iambC9EM',
        'chat_id': '6411380646'
    }
    
    # Optional Gemini config (you can provide API key if you have one)
    gemini_config = {
        'api_key': os.environ.get('GEMINI_API_KEY')  # Optional
    }
    
    print("📱 Telegram: CONFIGURED")
    if gemini_config.get('api_key'):
        print("🤖 Gemini AI: ENABLED")
    else:
        print("🤖 Gemini AI: Not configured (optional)")
    
    # Create monitor
    monitor = Global24x7JobMonitor(email_config, telegram_config, gemini_config)
    
    print(f"\n🔍 Running single global scan test...")
    print(f"⏰ Time: {datetime.datetime.now().strftime('%H:%M:%S')}")
    
    # Run one scan
    new_jobs = monitor.global_24x7_scan()
    
    print(f"\n📊 TEST RESULTS:")
    print(f"🎯 New jobs found: {new_jobs}")
    print(f"📱 Alert sent: {'YES' if new_jobs > 0 else 'NO'}")
    
    if new_jobs > 0:
        print(f"\n✅ SUCCESS! Found {new_jobs} real testing jobs!")
        print("🚀 Ready to start 24/7 monitoring")
        print("\nTo start continuous monitoring, run:")
        print("python global_24x7_realtime_monitor.py")
    else:
        print("\nℹ️ No new jobs in this test scan")
        print("💡 This is normal - the system will find new jobs as they're posted")
    
    print(f"\n🔄 24/7 Monitoring features:")
    print(f"   • Scans every 90 seconds")
    print(f"   • Covers RemoteOK, Indeed, Stack Overflow, WeWorkRemotely")
    print(f"   • Instant Telegram alerts")
    print(f"   • Targets 2+ years experience")
    print(f"   • Worldwide coverage")
    
    return new_jobs

if __name__ == "__main__":
    test_global_monitor()
