# Indeed Job Monitor Bot

Automated bot that monitors Indeed for software testing jobs with 2-6 years experience worldwide and sends email notifications.

## Features

- 🔍 Monitors Indeed job postings across multiple countries
- 📧 Email notifications for new job postings
- ⏰ Automated scheduling with GitHub Actions
- 🌍 Worldwide job search coverage
- 📊 Tracks previously seen jobs to avoid duplicates

## Setup Instructions

### 1. Fork this repository

### 2. Set up email configuration
Go to your repository Settings > Secrets and variables > Actions, and add:

- `SENDER_EMAIL`: Your Gmail address
- `EMAIL_APP_PASSWORD`: Your Gmail app password
- `RECIPIENT_EMAIL`: Email where you want to receive notifications

### 3. Enable GitHub Actions
- Go to Actions tab in your repository
- Enable workflows if prompted

### 4. Manual trigger (optional)
- Go to Actions > Indeed Job Monitor
- Click "Run workflow" to test immediately

## How it works

1. The bot searches Indeed across multiple countries
2. Filters jobs for software testing roles with 2-6 years experience
3. Compares with previously tracked jobs
4. Sends email notifications for new matches
5. Updates the tracked jobs database

## Schedule

The bot runs automatically every 6 hours. You can modify the schedule in `.github/workflows/job_monitor.yml`.

## Email Configuration

### Setting up Gmail App Password

1. Go to your Google Account settings
2. Enable 2-Factor Authentication if not already enabled
3. Go to Security > App passwords
4. Generate a new app password for "Mail"
5. Use this app password (not your regular password) in the `EMAIL_APP_PASSWORD` secret

## Countries Supported

- 🇺🇸 United States (indeed.com)
- 🇬🇧 United Kingdom (indeed.co.uk)
- 🇨🇦 Canada (indeed.ca)
- 🇦🇺 Australia (indeed.com.au)
- 🇮🇳 India (in.indeed.com)
- 🇩🇪 Germany (de.indeed.com)
- 🇫🇷 France (fr.indeed.com)

## Customization

You can modify the following in `job_monitor.py`:

- **Search terms**: Modify the `search_terms` variable
- **Experience level**: Adjust the `experience_keywords` list
- **Countries**: Update the `countries` parameter in `scrape_jobs()`
- **Frequency**: Change the cron schedule in the workflow file
- **Number of jobs per country**: Modify the slice `[:10]` in the scraping loop

## Testing Locally

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set environment variables:
   ```bash
   set SENDER_EMAIL=your-email@gmail.com
   set EMAIL_APP_PASSWORD=your-app-password
   set RECIPIENT_EMAIL=recipient@gmail.com
   ```
4. Run: `python job_monitor.py`

## Troubleshooting

- **No emails received**: Check your Gmail app password and spam folder
- **Workflow fails**: Check the Actions tab for error logs
- **Too many/few results**: Adjust the filtering keywords in the code

## Legal Notice

This bot uses web scraping for educational purposes. Please ensure compliance with Indeed's terms of service and robots.txt file. The bot includes respectful rate limiting and follows ethical scraping practices.
