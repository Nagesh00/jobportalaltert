@echo off
echo 🚨 STARTING REAL-TIME JOB MONITORING 🚨
echo ======================================
echo.
echo Your bot will scan for NEW testing jobs every 2 minutes
echo and send INSTANT Telegram alerts!
echo.
echo Press Ctrl+C to stop monitoring
echo.

REM Set environment variables
set TELEGRAM_BOT_TOKEN=8305949318:AAF257TSUv4EObGWLAAi7Cq7K87iambC9EM
set TELEGRAM_CHAT_ID=6411380646
set SENDER_EMAIL=kalyogyogi@gmail.com
set RECIPIENT_EMAIL=kalyogyogi@gmail.com

REM Start the enhanced real-time monitor
python enhanced_realtime_monitor.py

pause
