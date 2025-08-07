@echo off
echo ===============================================
echo    🔥 ULTRA REAL-TIME 24/7 JOB MONITORING
echo ===============================================
echo.
echo ⚡ ULTRA-FAST: 15-second continuous scans
echo 🎯 LASER-FOCUSED: Testing jobs ONLY
echo 📧 Target email: kalyogyogi@gmail.com
echo 🚨 Instant alerts: EVERY testing job found
echo � Operation: CONTINUOUS 24/7 - NEVER STOPS
echo.

cd /d "c:\Users\Nagnath\jobportal"

REM Set environment variables for ultra real-time monitoring
if not defined TELEGRAM_BOT_TOKEN set TELEGRAM_BOT_TOKEN=8305949318:AAF257TSUv4EObGWLAAi7Cq7K87iambC9EM
if not defined TELEGRAM_CHAT_ID set TELEGRAM_CHAT_ID=6411380646
if not defined GEMINI_API_KEY set GEMINI_API_KEY=AIzaSyDWzLu8s7KV4xSjjd0rUJSKxd2dC6Isljg

echo 📱 Telegram Bot: %TELEGRAM_BOT_TOKEN:~0,20%...
echo 📱 Chat ID: %TELEGRAM_CHAT_ID%
echo 🤖 Gemini AI: ENABLED for smart job analysis
echo.

echo 🔥 Starting ULTRA REAL-TIME 24/7 monitoring...
echo ⚡ Scanning every 15 seconds CONTINUOUSLY
echo 🎯 Testing jobs ONLY (QA, Automation, SDET, etc.)
echo 🚨 INSTANT alerts for every testing job found
echo 🔄 THIS RUNS 24/7 UNTIL MANUALLY STOPPED
echo.
echo 📱 Check Telegram for startup confirmation
echo Press Ctrl+C ONLY when you want to stop 24/7 monitoring
echo.

python ultra_realtime_24x7_monitor.py

pause
