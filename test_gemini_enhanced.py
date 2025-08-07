#!/usr/bin/env python3
"""
Test Gemini AI Enhanced Job Monitor
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set environment variables
os.environ['GEMINI_API_KEY'] = 'AIzaSyDWzLu8s7KV4xSjjd0rUJSKxd2dC6Isljg'
os.environ['TELEGRAM_BOT_TOKEN'] = '8305949318:AAF257TSUv4EObGWLAAi7Cq7K87iambC9EM'
os.environ['TELEGRAM_CHAT_ID'] = '6411380646'

from global_24x7_realtime_monitor import Global24x7JobMonitor
import datetime

def test_gemini_enhanced_monitor():
    print("🤖 TESTING GEMINI AI ENHANCED MONITOR")
    print("=" * 60)
    
    # Configuration with Gemini AI
    email_config = {
        'sender_email': 'kalyogyogi@gmail.com',
        'app_password': os.environ.get('EMAIL_APP_PASSWORD'),
        'recipient_email': 'kalyogyogi@gmail.com'
    }
    
    telegram_config = {
        'bot_token': '8305949318:AAF257TSUv4EObGWLAAi7Cq7K87iambC9EM',
        'chat_id': '6411380646'
    }
    
    # Gemini AI configuration
    gemini_config = {
        'api_key': 'AIzaSyDWzLu8s7KV4xSjjd0rUJSKxd2dC6Isljg'
    }
    
    print("📱 Telegram: CONFIGURED")
    print("🤖 Gemini AI: ENABLED for smart job analysis")
    print("🎯 Target: Software Testing (2+ years experience)")
    
    # Create enhanced monitor
    monitor = Global24x7JobMonitor(email_config, telegram_config, gemini_config)
    
    print(f"\n🔍 Running AI-enhanced global scan...")
    print(f"⏰ Time: {datetime.datetime.now().strftime('%H:%M:%S')}")
    print("🤖 Jobs will be analyzed by Gemini AI for relevance")
    
    # Run one enhanced scan
    new_jobs = monitor.global_24x7_scan()
    
    print(f"\n📊 GEMINI AI TEST RESULTS:")
    print(f"🎯 New jobs found: {new_jobs}")
    print(f"🤖 AI analysis: ENABLED")
    print(f"📱 Alert sent: {'YES' if new_jobs > 0 else 'NO'}")
    
    if new_jobs > 0:
        print(f"\n✅ SUCCESS! Found {new_jobs} AI-analyzed testing jobs!")
        print("🚀 Gemini AI will score each job for relevance")
        print("🎯 Only the best matches for 2+ years experience")
    else:
        print("\nℹ️ No new jobs in this scan (normal initially)")
        print("🤖 AI analysis ready for when new jobs are found")
    
    print(f"\n🤖 Gemini AI Features:")
    print(f"   • Job relevance scoring (1-10)")
    print(f"   • Experience level matching")
    print(f"   • Key requirements extraction")
    print(f"   • Smart filtering for testing roles")
    
    print(f"\n🚀 To start 24/7 AI-enhanced monitoring:")
    print(f"   start_global_24x7.bat")
    
    return new_jobs

if __name__ == "__main__":
    test_gemini_enhanced_monitor()
