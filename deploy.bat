@echo off
echo 🚀 Indeed Job Monitor Bot - GitHub Deployment Script
echo ==================================================

REM Check if git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git is not installed. Please install Git first.
    pause
    exit /b 1
)

REM Initialize git repository if not already
if not exist ".git" (
    echo 📁 Initializing Git repository...
    git init
    git branch -M main
)

REM Add all files
echo 📝 Adding files to Git...
git add .

REM Commit files
echo 💾 Committing files...
git commit -m "Initial commit: Indeed Job Monitor Bot"

echo.
echo ✅ Project setup complete!
echo.
echo 📋 Next steps to deploy on GitHub:
echo 1. Create a new repository on GitHub
echo 2. Copy the repository URL
echo 3. Run: git remote add origin ^<your-repository-url^>
echo 4. Run: git push -u origin main
echo.
echo 🔧 After pushing to GitHub:
echo 1. Go to Settings ^> Secrets and variables ^> Actions
echo 2. Add these secrets:
echo    - SENDER_EMAIL: Your Gmail address
echo    - EMAIL_APP_PASSWORD: Your Gmail app password
echo    - RECIPIENT_EMAIL: Email to receive notifications
echo 3. Go to Actions tab and enable workflows
echo 4. Manually trigger the workflow to test
echo.
echo 📧 Gmail App Password Setup:
echo 1. Enable 2FA on your Google account
echo 2. Go to Google Account ^> Security ^> App passwords
echo 3. Generate app password for 'Mail'
echo 4. Use this 16-digit password as EMAIL_APP_PASSWORD
echo.
echo 🎯 The bot will automatically run every 6 hours and send email notifications!

pause
