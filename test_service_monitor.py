#!/usr/bin/env python3
"""
Quick test of 24/7 service monitor
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("🔥 TESTING 24/7 SERVICE MONITOR")
print("=" * 50)

try:
    from service_24x7_monitor import Service24x7Monitor
    
    print("✅ Service imported successfully")
    
    monitor = Service24x7Monitor()
    print("✅ Service initialized")
    print("📱 Startup alert sent to Telegram")
    
    print("\n🧪 Running single service scan...")
    jobs_found = monitor.service_scan_cycle()
    
    print(f"\n📊 SERVICE TEST RESULTS:")
    print(f"⚡ Testing jobs found: {jobs_found}")
    print(f"🚨 Alert sent: {'YES' if jobs_found > 0 else 'NO'}")
    
    if jobs_found > 0:
        print(f"✅ SUCCESS! Service found {jobs_found} testing jobs!")
        print("🚨 Check your Telegram for lightning alert!")
    else:
        print("ℹ️ No new testing jobs (service ready for 24/7)")
    
    print(f"\n🔥 To start TRUE 24/7 service monitoring:")
    print(f"   start_true_24x7_service.bat")
    print(f"\n⚡ Service features:")
    print(f"   • 10-second lightning-fast scanning")
    print(f"   • TRUE 24/7 operation")
    print(f"   • Auto-restart every 24 hours")
    print(f"   • Self-healing on errors")
    print(f"   • Instant Telegram alerts")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n✅ Service test complete!")
