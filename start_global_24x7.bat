@echo off
echo ===============================================
echo    24/7 GLOBAL REAL-TIME JOB MONITORING
echo ===============================================
echo.
echo Starting worldwide job monitoring for software testing positions (2+ years)
echo Target email: kalyogyogi@gmail.com
echo Scan frequency: Every 90 seconds
echo.

cd /d "c:\Users\Nagnath\jobportal"

REM Set environment variables if not already set
if not defined TELEGRAM_BOT_TOKEN set TELEGRAM_BOT_TOKEN=8305949318:AAF257TSUv4EObGWLAAi7Cq7K87iambC9EM
if not defined TELEGRAM_CHAT_ID set TELEGRAM_CHAT_ID=6411380646
if not defined GEMINI_API_KEY set GEMINI_API_KEY=AIzaSyDWzLu8s7KV4xSjjd0rUJSKxd2dC6Isljg

echo Telegram Bot: %TELEGRAM_BOT_TOKEN:~0,20%...
echo Chat ID: %TELEGRAM_CHAT_ID%
echo Gemini AI: ENABLED for smart job analysis
echo.

echo Starting 24/7 monitoring...
echo Press Ctrl+C to stop monitoring
echo.

python debugged_24x7_monitor.py

pause
