@echo off
echo ============================================
echo    SETTING UP AUTOMATIC STARTUP
echo ============================================
echo.
echo This will make your job monitor start automatically 
echo when Windows boots up.
echo.
echo The monitor will run in the background and send
echo you instant Telegram alerts for new testing jobs.
echo.
pause

echo.
echo Creating Windows Task...

:: Create Windows Task Scheduler entry
schtasks /create /tn "Automatic Job Monitor 24x7" /tr "\"%~dp0START_AUTOMATIC_24X7.bat\"" /sc onstart /ru "SYSTEM" /f

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ SUCCESS! Automatic startup configured!
    echo.
    echo 🚀 Your job monitor will now:
    echo    • Start automatically when Windows boots
    echo    • Run in background 24/7
    echo    • Send instant Telegram alerts
    echo    • Monitor 5 job sources worldwide
    echo.
    echo 📱 You will receive a startup notification
    echo    in Telegram when the system starts.
    echo.
    echo 🛑 To disable automatic startup, run:
    echo    schtasks /delete /tn "Automatic Job Monitor 24x7"
    echo.
) else (
    echo.
    echo ❌ Could not create automatic startup.
    echo Please run this as Administrator.
    echo.
)

echo.
echo Starting monitor now for testing...
echo.
pause

call "%~dp0START_AUTOMATIC_24X7.bat"
