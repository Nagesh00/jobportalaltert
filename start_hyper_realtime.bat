@echo off
echo =======================================================
echo    🔥 HYPER-AGGRESSIVE REAL-TIME TESTING JOB MONITOR
echo =======================================================
echo.
echo ⚡ ULTRA-FAST: 30-second scan intervals
echo 🎯 LASER-FOCUSED: Testing jobs ONLY
echo 📧 TARGET: kalyogyogi@gmail.com
echo 🚨 INSTANT ALERTS: Maximum priority Telegram notifications
echo.

cd /d "c:\Users\Nagnath\jobportal"

REM Set environment variables for hyper-aggressive monitoring
set TELEGRAM_BOT_TOKEN=8305949318:AAF257TSUv4EObGWLAAi7Cq7K87iambC9EM
set TELEGRAM_CHAT_ID=6411380646
set GEMINI_API_KEY=AIzaSyDWzLu8s7KV4xSjjd0rUJSKxd2dC6Isljg

echo 📱 Telegram Bot: %TELEGRAM_BOT_TOKEN:~0,20%...
echo 📱 Chat ID: %TELEGRAM_CHAT_ID%
echo 🤖 Gemini AI: ENABLED
echo.

echo 🔥 Starting HYPER-AGGRESSIVE monitoring...
echo ⚡ Scanning every 30 seconds for testing jobs
echo 🎯 Filtering for: QA, Testing, Automation, SDET roles
echo 📧 Experience level: 2+ years
echo 🚨 INSTANT alerts for every testing job found
echo.
echo Press Ctrl+C to stop monitoring
echo.

python hyper_realtime_testing_monitor.py

pause
