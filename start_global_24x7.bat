@echo off
echo ===============================================
echo    🔥 HYPER-AGGRESSIVE REAL-TIME JOB MONITORING
echo ===============================================
echo.
echo ⚡ ULTRA-FAST: 30-second scans for testing jobs ONLY
echo 📧 Target email: kalyogyogi@gmail.com
echo 🎯 Focus: Software Testing (2+ years experience)
echo 🚨 Instant alerts: Maximum priority notifications
echo.

cd /d "c:\Users\Nagnath\jobportal"

REM Set environment variables for hyper-aggressive monitoring
if not defined TELEGRAM_BOT_TOKEN set TELEGRAM_BOT_TOKEN=8305949318:AAF257TSUv4EObGWLAAi7Cq7K87iambC9EM
if not defined TELEGRAM_CHAT_ID set TELEGRAM_CHAT_ID=6411380646
if not defined GEMINI_API_KEY set GEMINI_API_KEY=AIzaSyDWzLu8s7KV4xSjjd0rUJSKxd2dC6Isljg

echo 📱 Telegram Bot: %TELEGRAM_BOT_TOKEN:~0,20%...
echo 📱 Chat ID: %TELEGRAM_CHAT_ID%
echo 🤖 Gemini AI: ENABLED for smart job analysis
echo.

echo 🔥 Starting HYPER-AGGRESSIVE monitoring...
echo ⚡ Scanning every 30 seconds
echo 🎯 Testing jobs ONLY (QA, Automation, SDET, etc.)
echo 🚨 INSTANT alerts for every testing job found
echo Press Ctrl+C to stop monitoring
echo.

python hyper_realtime_testing_monitor.py

pause
