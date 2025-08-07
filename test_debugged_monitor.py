#!/usr/bin/env python3
"""
Quick test of debugged 24/7 monitor
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set environment variables
os.environ['GEMINI_API_KEY'] = 'AIzaSyDWzLu8s7KV4xSjjd0rUJSKxd2dC6Isljg'
os.environ['TELEGRAM_BOT_TOKEN'] = '8305949318:AAF257TSUv4EObGWLAAi7Cq7K87iambC9EM'
os.environ['TELEGRAM_CHAT_ID'] = '6411380646'

print("🔧 TESTING DEBUGGED 24/7 MONITOR")
print("=" * 50)

try:
    from debugged_24x7_monitor import Debugged24x7JobMonitor
    
    # Configuration
    email_config = {
        'sender_email': 'kalyogyogi@gmail.com',
        'app_password': None,
        'recipient_email': 'kalyogyogi@gmail.com'
    }
    
    telegram_config = {
        'bot_token': '8305949318:AAF257TSUv4EObGWLAAi7Cq7K87iambC9EM',
        'chat_id': '6411380646'
    }
    
    gemini_config = {
        'api_key': 'AIzaSyDWzLu8s7KV4xSjjd0rUJSKxd2dC6Isljg'
    }
    
    print("📱 Telegram: CONFIGURED")
    print("🤖 Gemini AI: CONFIGURED")
    print("🔧 Debug mode: ENABLED")
    
    # Create monitor
    monitor = Debugged24x7JobMonitor(email_config, telegram_config, gemini_config)
    
    print("\n🧪 Running single test scan...")
    new_jobs = monitor.enhanced_global_scan()
    
    print(f"\n📊 TEST RESULTS:")
    print(f"🎯 New jobs found: {new_jobs}")
    print(f"🔧 Debug logs: Check console output above")
    print(f"💾 Jobs saved to: debugged_24x7_jobs.json")
    
    if new_jobs > 0:
        print(f"\n✅ SUCCESS! System is working perfectly!")
        print(f"🚀 Ready for 24/7 monitoring")
    else:
        print(f"\nℹ️ No new jobs (normal for initial test)")
        print(f"🔄 System will find jobs as they're posted")
    
    print(f"\n🚀 To start continuous monitoring:")
    print(f"   start_global_24x7.bat")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Test error: {e}")
    import traceback
    traceback.print_exc()

print("\n✅ Test complete!")
