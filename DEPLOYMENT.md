# 🚀 Complete Deployment Guide

## Step-by-Step GitHub Deployment

### 1. Prerequisites
- GitHub account
- Gmail account with 2FA enabled
- Git installed on your computer

### 2. Create GitHub Repository
1. Go to [GitHub](https://github.com)
2. Click "New" repository
3. Name it: `indeed-job-monitor`
4. Make it **Public** (required for free GitHub Actions)
5. Don't initialize with README (we already have one)
6. Click "Create repository"

### 3. Upload Your Code
Run these commands in your terminal:

```bash
# Navigate to your project folder
cd "c:\Users\Nagnath\jobportal"

# Initialize Git (if not done)
git init
git branch -M main

# Add your files
git add .
git commit -m "Initial commit: Indeed Job Monitor Bot"

# Connect to GitHub (replace with your repo URL)
git remote add origin https://github.com/YOUR-USERNAME/indeed-job-monitor.git
git push -u origin main
```

### 4. Set Up Gmail App Password
1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Enable **2-Step Verification** if not already enabled
3. Go to **App passwords**
4. Select "Mail" and generate password
5. **Copy the 16-digit password** (you'll need it for GitHub secrets)

### 5. Configure GitHub Secrets
1. Go to your GitHub repository
2. Click **Settings** tab
3. Click **Secrets and variables** > **Actions**
4. Click **New repository secret** for each:

   - **Name:** `SENDER_EMAIL`
     **Value:** your-email@gmail.com

   - **Name:** `EMAIL_APP_PASSWORD`
     **Value:** your-16-digit-app-password

   - **Name:** `RECIPIENT_EMAIL`
     **Value:** email-to-receive-notifications@gmail.com

### 6. Enable GitHub Actions
1. Go to **Actions** tab in your repository
2. Click **Enable workflows** if prompted
3. You should see "Indeed Job Monitor" workflow

### 7. Test the Bot
1. In Actions tab, click **Indeed Job Monitor**
2. Click **Run workflow** > **Run workflow**
3. Wait for it to complete (green checkmark)
4. Check your email for notifications

## 🔧 Customization Options

### Change Search Frequency
Edit `.github/workflows/job_monitor.yml`:
```yaml
schedule:
  - cron: '0 */4 * * *'  # Every 4 hours
  - cron: '0 9,17 * * *'  # 9 AM and 5 PM daily
```

### Modify Search Terms
Edit `job_monitor.py`, line 25:
```python
search_terms = "qa automation engineer 2 to 6 years"
```

### Add/Remove Countries
Edit `job_monitor.py`, line 50:
```python
countries=["US", "UK", "CA", "AU", "IN", "DE"]
```

### Change Experience Range
Edit `job_monitor.py`, lines 140-143:
```python
experience_keywords = [
    '1 year', '2 year', '3 year', '4 year',
    '1-2', '2-3', '3-4'
]
```

## 📊 Monitoring and Troubleshooting

### Check Bot Status
- Go to **Actions** tab to see execution history
- Green checkmark = successful run
- Red X = failed run (click to see error details)

### Common Issues

**No emails received:**
- Check spam folder
- Verify Gmail app password is correct
- Ensure 2FA is enabled on Gmail

**Workflow fails:**
- Check if secrets are set correctly
- Look at error logs in Actions tab
- Ensure repository is public for free Actions

**Too many/few results:**
- Adjust keywords in `is_relevant_job()` function
- Modify experience keywords
- Change country list

### View Tracked Jobs
The bot saves all found jobs in `tracked_jobs.json` in your repository.

## 🎯 Expected Results

- **Frequency:** Runs every 6 hours automatically
- **Coverage:** 5+ countries simultaneously  
- **Filtering:** Only relevant software testing jobs with 2-6 years experience
- **Notifications:** HTML-formatted emails with job details
- **Tracking:** Prevents duplicate notifications

## 📈 Usage Statistics

After deployment, you can monitor:
- Number of jobs found per run (in Actions logs)
- Countries with most opportunities
- Success rate of email delivery
- Total jobs tracked over time

## 🚨 Important Notes

- **Rate Limiting:** Bot includes delays to respect Indeed's servers
- **Legal:** Uses ethical web scraping practices
- **Cost:** Completely free using GitHub Actions (2000 minutes/month)
- **Reliability:** GitHub Actions has 99.9% uptime

Your bot is now ready to monitor Indeed jobs 24/7 and send you instant notifications! 🎉
