#!/usr/bin/env python3
"""
Quick test of hyper-aggressive testing monitor
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("🔥 TESTING HYPER-AGGRESSIVE MONITOR")
print("=" * 50)

try:
    from hyper_realtime_testing_monitor import HyperRealtimeTestingMonitor
    
    print("✅ Monitor imported successfully")
    
    monitor = HyperRealtimeTestingMonitor()
    print("✅ Monitor initialized")
    
    print("\n🧪 Running single hyper-aggressive scan...")
    jobs_found = monitor.hyper_aggressive_scan()
    
    print(f"\n📊 RESULTS:")
    print(f"🎯 Testing jobs found: {jobs_found}")
    print(f"🚨 Alert sent: {'YES' if jobs_found > 0 else 'NO'}")
    
    if jobs_found > 0:
        print(f"✅ SUCCESS! Found {jobs_found} testing-specific jobs!")
        print("🚨 Check your Telegram for instant alert!")
    else:
        print("ℹ️ No new testing jobs (will find them as posted)")
    
    print(f"\n🔥 To start hyper-aggressive monitoring:")
    print(f"   start_hyper_realtime.bat")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n✅ Test complete!")
