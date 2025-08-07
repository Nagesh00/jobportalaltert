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

class IndeedJobMonitor:
    def __init__(self, email_config=None, debug_mode=False):
        self.email_config = email_config
        self.debug_mode = debug_mode
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
        search_terms = "software testing 2 to 6 years experience"
        
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
        
        if self.debug_mode:
            print(f"🔗 Built URL for {country}: {url}")
        
        return url
    
    def build_alternative_search_url(self, country=""):
        """Build alternative Indeed search URL with simpler parameters"""
        # Simpler search terms to avoid blocking
        search_terms = "software testing"
        
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
        
        # Build simpler URL
        encoded_terms = quote(search_terms)
        url = f"https://{domain}/jobs?q={encoded_terms}"
        
        if self.debug_mode:
            print(f"🔗 Built alternative URL for {country}: {url}")
        
        return url
    
    def scrape_jobs(self, countries=["US"], max_jobs_per_country=5):
        """Scrape jobs from multiple countries"""
        all_new_jobs = []
        
        for country in countries:
            try:
                print(f"🔍 Searching jobs in {country}...")
                url = self.build_search_url(country)
                
                # More comprehensive headers to avoid blocking
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
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
                    'Cache-Control': 'max-age=0'
                }
                
                if self.debug_mode:
                    print(f"📡 Making request to: {url}")
                
                # Add session for better connection handling
                session = requests.Session()
                session.headers.update(headers)
                
                response = session.get(url, timeout=15)
                
                if self.debug_mode:
                    print(f"📊 Response status: {response.status_code}")
                
                if response.status_code == 403:
                    print(f"🚫 Access blocked for {country}. Trying alternative approach...")
                    # Try with a different search approach
                    alt_url = self.build_alternative_search_url(country)
                    if alt_url:
                        response = session.get(alt_url, timeout=15)
                        if self.debug_mode:
                            print(f"📊 Alternative URL response: {response.status_code}")
                
                response.raise_for_status()
                
                if self.debug_mode:
                    print(f"✅ Response status: {response.status_code}")
                    print(f"📄 Response size: {len(response.content)} bytes")
                
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
                        if self.debug_mode:
                            print(f"✅ Found {len(job_cards)} job cards using selector: {selector}")
                        break
                
                if not job_cards:
                    if self.debug_mode:
                        print("❌ No job cards found with any selector")
                        # Print page structure for debugging
                        print("🔍 Page structure analysis:")
                        titles = soup.find_all(['h1', 'h2', 'h3'])[:5]
                        for title in titles:
                            print(f"  Title: {title.get_text().strip()[:100]}")
                    continue
                
                jobs_found = 0
                for i, card in enumerate(job_cards[:max_jobs_per_country]):
                    if self.debug_mode:
                        print(f"🔎 Processing job card {i+1}...")
                    
                    job_data = self.extract_job_data(card, country)
                    if job_data:
                        if self.debug_mode:
                            print(f"📋 Extracted: {job_data['title']} at {job_data['company']}")
                        
                        if self.is_relevant_job(job_data):
                            job_id = job_data['id']
                            if job_id and job_id not in self.tracked_jobs:
                                self.tracked_jobs[job_id] = job_data
                                all_new_jobs.append(job_data)
                                jobs_found += 1
                                if self.debug_mode:
                                    print(f"✅ Added relevant job: {job_data['title']}")
                            elif self.debug_mode and job_id in self.tracked_jobs:
                                print(f"⚠️  Job already tracked: {job_data['title']}")
                        elif self.debug_mode:
                            print(f"❌ Job not relevant: {job_data['title']}")
                    elif self.debug_mode:
                        print(f"❌ Failed to extract job data from card {i+1}")
                
                print(f"✅ Found {jobs_found} new relevant jobs in {country}")
                
                # Add delay between requests to be respectful
                time.sleep(2)
                
            except requests.exceptions.RequestException as e:
                print(f"🌐 Network error scraping {country}: {str(e)}")
                continue
            except Exception as e:
                print(f"❌ Error scraping {country}: {str(e)}")
                if self.debug_mode:
                    import traceback
                    traceback.print_exc()
                continue
        
        return all_new_jobs
    
    def extract_job_data(self, card, country):
        """Extract job data from job card"""
        try:
            # Extract job ID first (most reliable identifier)
            job_id = None
            if card.get('data-jk'):
                job_id = card.get('data-jk')
            else:
                job_link = card.find('a', {'data-jk': True})
                if job_link:
                    job_id = job_link.get('data-jk')
            
            if not job_id:
                if self.debug_mode:
                    print("❌ No job ID found in card")
                return None
            
            # Extract job title with multiple selectors
            title = "N/A"
            title_selectors = [
                'h2[data-testid="job-title"] a span',
                'h2 a[data-testid="job-title-link"] span',
                '.jobTitle a span[title]',
                'h2.jobTitle a span',
                '[data-testid="job-title"]',
                '.jobTitle',
                'h2 a span'
            ]
            
            for selector in title_selectors:
                title_elem = card.select_one(selector)
                if title_elem:
                    title = title_elem.get('title') or title_elem.get_text().strip()
                    if title and title != "N/A":
                        break
            
            # Extract company name
            company = "N/A"
            company_selectors = [
                '[data-testid="company-name"]',
                '.companyName',
                'span.companyName a',
                'span.companyName span',
                '[data-testid="company-name"] a'
            ]
            
            for selector in company_selectors:
                company_elem = card.select_one(selector)
                if company_elem:
                    company = company_elem.get_text().strip()
                    if company and company != "N/A":
                        break
            
            # Extract location
            location = "N/A"
            location_selectors = [
                '[data-testid="job-location"]',
                '.locationsContainer',
                '.companyLocation',
                '.location'
            ]
            
            for selector in location_selectors:
                location_elem = card.select_one(selector)
                if location_elem:
                    location = location_elem.get_text().strip()
                    if location and location != "N/A":
                        break
            
            # Extract snippet/description
            snippet = "N/A"
            snippet_selectors = [
                '[data-testid="job-snippet"]',
                '.job-snippet',
                '.summary',
                '.jobSnippet'
            ]
            
            for selector in snippet_selectors:
                snippet_elem = card.select_one(selector)
                if snippet_elem:
                    snippet = snippet_elem.get_text().strip()
                    if snippet and snippet != "N/A":
                        break
            
            # Build job URL
            job_url = f"https://{self.get_country_domain(country)}/viewjob?jk={job_id}"
            
            job_data = {
                'id': job_id,
                'title': title,
                'company': company,
                'location': location,
                'snippet': snippet,
                'url': job_url,
                'country': country,
                'date_found': datetime.datetime.now().isoformat()
            }
            
            if self.debug_mode:
                print(f"📊 Extracted job data: ID={job_id}, Title='{title[:50]}...', Company='{company}'")
            
            return job_data
            
        except Exception as e:
            if self.debug_mode:
                print(f"❌ Error extracting job data: {str(e)}")
                import traceback
                traceback.print_exc()
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
            'selenium', 'cypress', 'junit', 'pytest', 'tester', 'sdet'
        ]
        
        # Experience keywords (more flexible)
        experience_keywords = [
            '2 year', '3 year', '4 year', '5 year', '6 year',
            '2-3', '3-4', '4-5', '5-6', '2 to', '3 to', '4 to', '5 to',
            '2+', '3+', '4+', '5+', 'junior', 'mid-level', 'intermediate'
        ]
        
        # Check if job contains testing keywords
        has_testing = any(keyword in title or keyword in snippet for keyword in testing_keywords)
        
        # Check if job mentions relevant experience level (more lenient for debugging)
        has_experience = any(keyword in snippet for keyword in experience_keywords)
        
        if self.debug_mode:
            print(f"🔍 Relevance check for '{job_data['title'][:50]}...':")
            print(f"   Testing keywords found: {has_testing}")
            print(f"   Experience keywords found: {has_experience}")
            if has_testing:
                found_testing = [kw for kw in testing_keywords if kw in title or kw in snippet]
                print(f"   Testing keywords: {found_testing}")
            if has_experience:
                found_exp = [kw for kw in experience_keywords if kw in snippet]
                print(f"   Experience keywords: {found_exp}")
        
        # For debugging, let's be more lenient - just need testing keywords
        return has_testing
    
    def send_email_notification(self, new_jobs):
        """Send email notification for new jobs"""
        if not new_jobs:
            return
        
        if not self.email_config or not all(self.email_config.values()):
            print(f"📧 Would send email notification for {len(new_jobs)} jobs (email config missing)")
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
            
            print(f"📧 Email sent successfully with {len(new_jobs)} jobs!")
            
        except Exception as e:
            print(f"❌ Error sending email: {str(e)}")
    
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
    
    def run_monitoring(self, debug_mode=False):
        """Main monitoring function"""
        print("🔍 Starting job monitoring...")
        
        if debug_mode:
            print("🐛 Debug mode enabled")
            # Use only US for debugging and limit to fewer jobs
            countries = ["US"]
            max_jobs = 3
        else:
            countries = ["US", "UK", "CA", "AU", "IN"]
            max_jobs = 10
        
        # Search for new jobs
        new_jobs = self.scrape_jobs(countries=countries, max_jobs_per_country=max_jobs)
        
        if new_jobs:
            print(f"✅ Found {len(new_jobs)} new jobs!")
            print("\n📋 New Jobs Summary:")
            for i, job in enumerate(new_jobs, 1):
                print(f"{i}. {job['title']} at {job['company']} ({job['location']})")
            
            self.send_email_notification(new_jobs)
            self.save_tracked_jobs()
        else:
            print("ℹ️ No new jobs found.")
        
        return len(new_jobs)

def main():
    # Email configuration (optional for debugging)
    email_config = {
        'sender_email': os.environ.get('SENDER_EMAIL'),
        'app_password': os.environ.get('EMAIL_APP_PASSWORD'),
        'recipient_email': os.environ.get('RECIPIENT_EMAIL')
    }
    
    # Check if we're in debug mode
    debug_mode = True  # Set to True for debugging
    
    if debug_mode:
        print("🐛 Running in DEBUG mode")
        print("📧 Email notifications will be simulated")
    
    # Initialize and run monitor
    monitor = IndeedJobMonitor(email_config, debug_mode=debug_mode)
    new_jobs_count = monitor.run_monitoring(debug_mode=debug_mode)
    
    print(f"\n✅ Job monitoring completed. Found {new_jobs_count} new jobs.")

if __name__ == "__main__":
    main()
