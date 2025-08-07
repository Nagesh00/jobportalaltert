import requests
from bs4 import BeautifulSoup
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
import time
import os
from urllib.parse import urljoin, quote
import random

class IndeedJobMonitor:
    def __init__(self, email_config, telegram_config=None):
        self.email_config = email_config
        self.telegram_config = telegram_config
        self.base_url = "https://indeed.com"
        self.jobs_file = "tracked_jobs.json"
        self.load_tracked_jobs()
        
    def load_tracked_jobs(self):
        """Load previously tracked jobs from file"""
        try:
            with open(self.jobs_file, 'r') as f:
                self.tracked_jobs = json.load(f)
        except FileNotFoundError:
            self.tracked_jobs = {}
    
    def save_tracked_jobs(self):
        """Save tracked jobs to file"""
        with open(self.jobs_file, 'w') as f:
            json.dump(self.tracked_jobs, f, indent=2)
    
    def build_search_url(self, country=""):
        """Build Indeed search URL for software testing jobs with 2-6 years experience"""
        # Search parameters for software testing jobs with 2-6 years experience
        search_terms = "software testing"  # Simplified to avoid blocking
        
        # Country-specific Indeed domains
        country_domains = {
            "US": "indeed.com",
            "UK": "indeed.co.uk", 
            "CA": "indeed.ca",
            "AU": "indeed.com.au",
            "IN": "in.indeed.com",
            "DE": "de.indeed.com",
            "FR": "fr.indeed.com"
        }
        
        domain = country_domains.get(country, "indeed.com")
        
        # Build URL with search parameters
        encoded_terms = quote(search_terms)
        url = f"https://{domain}/jobs?q={encoded_terms}&sort=date"
        
        return url
    
    def get_random_headers(self):
        """Get randomized headers to avoid detection"""
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ]
        
        headers = {
            'User-Agent': random.choice(user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
            'Referer': 'https://www.google.com/'
        }
        
        return headers
    
    def scrape_jobs(self, countries=["US", "UK", "CA", "AU", "IN"]):
        """Scrape jobs from multiple countries with anti-blocking measures"""
        all_new_jobs = []
        
        print("⚠️  Note: Indeed actively blocks automated requests.")
        print("🔄 Attempting to fetch jobs with anti-detection measures...")
        
        for country in countries:
            try:
                print(f"Searching jobs in {country}...")
                url = self.build_search_url(country)
                
                # Random delay to avoid rate limiting
                delay = random.uniform(3, 8)
                print(f"⏱️  Waiting {delay:.1f} seconds before request...")
                time.sleep(delay)
                
                headers = self.get_random_headers()
                
                # Use session for better connection handling
                session = requests.Session()
                session.headers.update(headers)
                
                # Try multiple times with different approaches
                max_retries = 3
                for attempt in range(max_retries):
                    try:
                        response = session.get(url, timeout=15)
                        
                        if response.status_code == 200:
                            print(f"✅ Successfully accessed {country}")
                            break
                        elif response.status_code == 403:
                            print(f"🚫 Access blocked for {country} (attempt {attempt + 1}/{max_retries})")
                            if attempt < max_retries - 1:
                                time.sleep(random.uniform(5, 10))
                        else:
                            print(f"❌ Status {response.status_code} for {country}")
                            
                    except requests.exceptions.RequestException as e:
                        print(f"🌐 Network error for {country}: {str(e)}")
                        if attempt < max_retries - 1:
                            time.sleep(random.uniform(3, 6))
                
                if response.status_code != 200:
                    print(f"❌ Failed to access {country} after {max_retries} attempts")
                    continue
                
                # Parse the response
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Try multiple selectors for job cards
                job_cards = []
                selectors = [
                    'div[data-jk]',
                    '.job_seen_beacon',
                    '.result',
                    '.slider_container .slider_item',
                    '[data-testid="job-title"]'
                ]
                
                for selector in selectors:
                    job_cards = soup.select(selector)
                    if job_cards:
                        break
                
                if not job_cards:
                    print(f"❌ No job cards found for {country}")
                    continue
                
                print(f"📋 Found {len(job_cards)} job cards in {country}")
                
                for card in job_cards[:10]:  # Limit to first 10 jobs per country
                    job_data = self.extract_job_data(card, country)
                    if job_data and self.is_relevant_job(job_data):
                        job_id = job_data['id']
                        if job_id not in self.tracked_jobs:
                            self.tracked_jobs[job_id] = job_data
                            all_new_jobs.append(job_data)
                
                # Add longer delay between countries
                if country != countries[-1]:  # Don't wait after the last country
                    time.sleep(random.uniform(10, 20))
                
            except Exception as e:
                print(f"Error scraping {country}: {str(e)}")
                continue
        
        return all_new_jobs
    
    def extract_job_data(self, card, country):
        """Extract job data from job card"""
        try:
            # Extract job title
            title_elem = card.find('h2', class_='jobTitle') or card.find('a', {'data-jk': True})
            title = title_elem.get_text().strip() if title_elem else "N/A"
            
            # Extract company name
            company_elem = card.find('span', class_='companyName') or card.find('span', {'data-testid': 'company-name'})
            company = company_elem.get_text().strip() if company_elem else "N/A"
            
            # Extract location
            location_elem = card.find('div', {'data-testid': 'job-location'}) or card.find('span', class_='locationsContainer')
            location = location_elem.get_text().strip() if location_elem else "N/A"
            
            # Extract job ID
            job_link = card.find('a', {'data-jk': True})
            job_id = job_link.get('data-jk') if job_link else None
            
            # Extract snippet/description
            snippet_elem = card.find('div', class_='job-snippet') or card.find('ul')
            snippet = snippet_elem.get_text().strip() if snippet_elem else "N/A"
            
            # Build job URL
            job_url = f"https://{self.get_country_domain(country)}/viewjob?jk={job_id}" if job_id else "N/A"
            
            return {
                'id': job_id,
                'title': title,
                'company': company,
                'location': location,
                'snippet': snippet,
                'url': job_url,
                'country': country,
                'date_found': datetime.datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error extracting job data: {str(e)}")
            return None
    
    def get_country_domain(self, country):
        """Get Indeed domain for country"""
        domains = {
            "US": "indeed.com",
            "UK": "indeed.co.uk",
            "CA": "indeed.ca", 
            "AU": "indeed.com.au",
            "IN": "in.indeed.com",
            "DE": "de.indeed.com",
            "FR": "fr.indeed.com"
        }
        return domains.get(country, "indeed.com")
    
    def is_relevant_job(self, job_data):
        """Check if job is relevant based on title and description"""
        title = job_data['title'].lower()
        snippet = job_data['snippet'].lower()
        
        # Keywords that indicate software testing roles
        testing_keywords = [
            'test', 'testing', 'qa', 'quality assurance', 'automation',
            'selenium', 'cypress', 'junit', 'pytest', 'tester'
        ]
        
        # Experience keywords
        experience_keywords = [
            '2 year', '3 year', '4 year', '5 year', '6 year',
            '2-3', '3-4', '4-5', '5-6', '2 to', '3 to', '4 to', '5 to'
        ]
        
        # Check if job contains testing keywords
        has_testing = any(keyword in title or keyword in snippet for keyword in testing_keywords)
        
        # Check if job mentions relevant experience level
        has_experience = any(keyword in snippet for keyword in experience_keywords)
        
        return has_testing and has_experience
    
    def send_telegram_notification(self, new_jobs):
        """Send Telegram notification for new jobs"""
        if not new_jobs or not self.telegram_config:
            return
            
        try:
            bot_token = self.telegram_config['bot_token']
            chat_id = self.telegram_config['chat_id']
            
            # Create message text
            message = f"🎯 *{len(new_jobs)} New Software Testing Jobs Found!*\n\n"
            
            for i, job in enumerate(new_jobs[:5], 1):  # Limit to 5 jobs per message
                message += f"*{i}. {job['title']}*\n"
                message += f"🏢 Company: {job['company']}\n"
                message += f"📍 Location: {job['location']} ({job['country']})\n"
                message += f"📝 {job['snippet'][:150]}...\n"
                message += f"🔗 [View Job]({job['url']})\n\n"
            
            if len(new_jobs) > 5:
                message += f"... and {len(new_jobs) - 5} more jobs!\n"
                message += f"Check your email for complete list.\n"
            
            # Send to Telegram
            telegram_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            data = {
                'chat_id': chat_id,
                'text': message,
                'parse_mode': 'Markdown',
                'disable_web_page_preview': True
            }
            
            response = requests.post(telegram_url, data=data, timeout=10)
            
            if response.status_code == 200:
                print(f"📱 Telegram notification sent successfully with {len(new_jobs)} jobs!")
            else:
                print(f"❌ Telegram notification failed: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"❌ Error sending Telegram notification: {str(e)}")
    
    def send_email_notification(self, new_jobs):
        """Send email notification for new jobs"""
        if not new_jobs:
            return
            
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_config['sender_email']
            msg['To'] = self.email_config['recipient_email']
            msg['Subject'] = f"🎯 {len(new_jobs)} New Software Testing Jobs Found!"
            
            # Create email body
            body = self.create_email_body(new_jobs)
            msg.attach(MIMEText(body, 'html'))
            
            # Send email
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.email_config['sender_email'], self.email_config['app_password'])
            
            text = msg.as_string()
            server.sendmail(self.email_config['sender_email'], self.email_config['recipient_email'], text)
            server.quit()
            
            print(f"Email sent successfully with {len(new_jobs)} jobs!")
            
        except Exception as e:
            print(f"Error sending email: {str(e)}")
    
    def create_email_body(self, jobs):
        """Create HTML email body"""
        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .job {{ border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px; }}
                .job-title {{ color: #2557a7; font-weight: bold; font-size: 18px; }}
                .company {{ color: #666; font-size: 16px; margin: 5px 0; }}
                .location {{ color: #888; font-size: 14px; }}
                .snippet {{ margin: 10px 0; font-size: 14px; }}
                .apply-btn {{ background-color: #2557a7; color: white; padding: 10px 20px; 
                           text-decoration: none; border-radius: 5px; display: inline-block; margin-top: 10px; }}
            </style>
        </head>
        <body>
            <h2>🎯 New Software Testing Jobs (2-6 Years Experience)</h2>
            <p>Found {len(jobs)} new jobs matching your criteria:</p>
        """
        
        for job in jobs:
            html += f"""
            <div class="job">
                <div class="job-title">{job['title']}</div>
                <div class="company">🏢 {job['company']}</div>
                <div class="location">📍 {job['location']} ({job['country']})</div>
                <div class="snippet">{job['snippet'][:200]}...</div>
                <a href="{job['url']}" class="apply-btn">View Job</a>
            </div>
            """
        
        html += """
        </body>
        </html>
        """
        
        return html
    
    def run_monitoring(self):
        """Main monitoring function"""
        print("🔍 Starting job monitoring...")
        
        # Search for new jobs
        new_jobs = self.scrape_jobs()
        
        if new_jobs:
            print(f"✅ Found {len(new_jobs)} new jobs!")
            
            # Send notifications
            if self.telegram_config:
                self.send_telegram_notification(new_jobs)
            
            if self.email_config and all(self.email_config.values()):
                self.send_email_notification(new_jobs)
            
            self.save_tracked_jobs()
        else:
            print("ℹ️ No new jobs found.")
        
        return len(new_jobs)

def main():
    # Email configuration
    email_config = {
        'sender_email': os.environ.get('SENDER_EMAIL'),
        'app_password': os.environ.get('EMAIL_APP_PASSWORD'),
        'recipient_email': os.environ.get('RECIPIENT_EMAIL')
    }
    
    # Telegram configuration
    telegram_config = {
        'bot_token': os.environ.get('TELEGRAM_BOT_TOKEN'),
        'chat_id': os.environ.get('TELEGRAM_CHAT_ID')
    }
    
    # Check if we have at least one notification method
    has_email = all(email_config.values())
    has_telegram = all(telegram_config.values())
    
    if not has_email and not has_telegram:
        print("❌ No notification configuration found!")
        print("Please set either email or Telegram environment variables.")
        return
    
    if has_telegram:
        print("📱 Telegram notifications enabled")
    if has_email:
        print("📧 Email notifications enabled")
    
    # Initialize and run monitor
    monitor = IndeedJobMonitor(email_config, telegram_config if has_telegram else None)
    new_jobs_count = monitor.run_monitoring()
    
    print(f"✅ Job monitoring completed. Found {new_jobs_count} new jobs.")

if __name__ == "__main__":
    main()
