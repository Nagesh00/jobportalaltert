@echo off
title AUTOMATIC 24/7 JOB MONITOR - STARTING...

echo ============================================
echo    AUTOMATIC 24/7 JOB MONITOR STARTING
echo ============================================
echo.
echo ⚡ This will run automatically forever
echo 📱 You will get instant Telegram alerts  
echo 🛑 Close this window to stop monitoring
echo.
echo Starting in 3 seconds...
timeout /t 3 /nobreak >nul

cls
echo ============================================
echo    AUTOMATIC MONITORING IS NOW ACTIVE
echo ============================================
echo.
echo ✅ System is running automatically
echo 📱 Check your Telegram for startup message
echo 🔄 Scanning every 10 seconds
echo 💼 Monitoring 5 job sources worldwide
echo.
echo ⚠️  KEEP THIS WINDOW OPEN
echo    Closing will stop job monitoring
echo.
echo ============================================

cd /d "%~dp0"
call .venv\Scripts\activate.bat

python automatic_24x7_monitor.py

echo.
echo ============================================
echo    AUTOMATIC MONITORING STOPPED
echo ============================================
pause
