# 🔧 GitHub Secrets Setup Instructions

## ✅ Your Email Configuration (kalyogyogi@gmail.com)

You need to add these secrets to your GitHub repository:

### 📧 Email Secrets:
```
SENDER_EMAIL: kalyogyogi@gmail.com
RECIPIENT_EMAIL: kalyogyogi@gmail.com
EMAIL_APP_PASSWORD: [Your Gmail App Password - see below]
```

### 📱 Telegram Secrets:
```
TELEGRAM_BOT_TOKEN: 8305949318:AAF257TSUv4EObGWLAAi7Cq7K87iambC9EM
TELEGRAM_CHAT_ID: 6411380646
```

## 🔐 How to Get Gmail App Password:

1. **Enable 2-Factor Authentication:**
   - Go to: https://myaccount.google.com/security
   - Turn on 2-Step Verification if not already enabled

2. **Generate App Password:**
   - Go to: https://myaccount.google.com/apppasswords
   - Select "Mail" and "Windows Computer" (or Other)
   - Copy the 16-character password (example: abcd efgh ijkl mnop)

3. **Add Secrets to GitHub:**
   - Go to your repository: https://github.com/Nagesh00/jobportalaltert
   - Click: Settings → Secrets and Variables → Actions
   - Click "New repository secret" for each secret above

## 🧪 Test Email Locally:

Before setting up GitHub secrets, test your email configuration:

```powershell
# Set your app password
$env:EMAIL_APP_PASSWORD="your-16-character-app-password"

# Run the email test
python test_email.py
```

## ⚡ Quick Setup Commands:

After getting your Gmail App Password, run these commands:

```powershell
# Test email configuration
$env:EMAIL_APP_PASSWORD="your-app-password-here"
python test_email.py

# Test real job monitoring (no demos)
$env:TELEGRAM_BOT_TOKEN="8305949318:AAF257TSUv4EObGWLAAi7Cq7K87iambC9EM"
$env:TELEGRAM_CHAT_ID="6411380646"
$env:SENDER_EMAIL="kalyogyogi@gmail.com"
$env:RECIPIENT_EMAIL="kalyogyogi@gmail.com"
python job_monitor_alternative.py
```

## 🎯 What's Fixed:

1. ✅ **Removed all demo jobs** - Only real jobs from RemoteOK and RSS feeds
2. ✅ **Updated email configuration** for kalyogyogi@gmail.com
3. ✅ **Fixed GitHub Actions permissions** for automatic updates
4. ✅ **Created email test script** to verify your setup

## 📱 Real-Time Monitoring:

Your bot will now:
- ✅ Find REAL software testing jobs (no demos)
- ✅ Send instant Telegram notifications
- ✅ Send detailed email alerts to kalyogyogi@gmail.com
- ✅ Run automatically every 6 hours on GitHub
- ✅ Track jobs to avoid duplicates

## 🚨 Important Notes:

1. **Gmail App Password** is different from your regular password
2. **Must enable 2-Factor Authentication** first
3. **App Password is 16 characters** with spaces (like: abcd efgh ijkl mnop)
4. **Keep App Password secure** - treat it like a password

Once you add the secrets to GitHub, your job monitor will run automatically! 🎉
