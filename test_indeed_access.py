import requests
import time
import random
from bs4 import BeautifulSoup
from urllib.parse import quote
import json

def test_indeed_access():
    """Test different approaches to access Indeed"""
    
    print("🔍 Testing Indeed access with different approaches...")
    
    # Test URLs
    test_urls = [
        "https://indeed.com/jobs?q=software+testing",
        "https://indeed.com/jobs?q=qa+engineer", 
        "https://indeed.com/jobs?q=test+engineer",
        "https://www.indeed.com/jobs?q=software+testing",
    ]
    
    # Different user agents to try
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    ]
    
    for i, url in enumerate(test_urls):
        print(f"\n🌐 Testing URL {i+1}: {url}")
        
        for j, ua in enumerate(user_agents):
            try:
                headers = {
                    'User-Agent': ua,
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                }
                
                print(f"  🤖 User Agent {j+1}: {ua[:50]}...")
                
                session = requests.Session()
                session.headers.update(headers)
                
                # Add random delay
                time.sleep(random.uniform(1, 3))
                
                response = session.get(url, timeout=10)
                
                print(f"    📊 Status: {response.status_code}")
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Check for common Indeed elements
                    job_elements = soup.find_all(['div'], class_=lambda x: x and 'job' in x.lower()) if soup else []
                    title_elements = soup.find_all(['h2', 'a'], attrs={'data-testid': lambda x: x and 'title' in x.lower()}) if soup else []
                    
                    print(f"    📄 Page size: {len(response.content)} bytes")
                    print(f"    🔍 Job elements found: {len(job_elements)}")
                    print(f"    📝 Title elements found: {len(title_elements)}")
                    
                    # Check for CAPTCHA or blocking
                    if soup and 'captcha' in response.text.lower():
                        print("    🚫 CAPTCHA detected")
                    elif soup and 'blocked' in response.text.lower():
                        print("    🚫 Blocking detected")
                    elif len(response.content) < 1000:
                        print("    ⚠️  Suspiciously small response")
                    else:
                        print("    ✅ Response looks good!")
                        
                        # Try to find job titles
                        titles = soup.find_all(['h2', 'a'], string=lambda x: x and any(word in x.lower() for word in ['engineer', 'developer', 'analyst', 'test']))[:3]
                        if titles:
                            print("    📋 Sample job titles found:")
                            for title in titles:
                                print(f"      - {title.get_text().strip()[:60]}...")
                        
                        return True, url, headers
                
                elif response.status_code == 403:
                    print("    🚫 403 Forbidden")
                elif response.status_code == 429:
                    print("    🐌 429 Rate Limited")
                else:
                    print(f"    ❌ Error: {response.status_code}")
                    
            except requests.exceptions.RequestException as e:
                print(f"    ❌ Request failed: {str(e)[:50]}...")
            except Exception as e:
                print(f"    ❌ Other error: {str(e)[:50]}...")
    
    return False, None, None

def test_alternative_job_sites():
    """Test alternative job sites that might be easier to scrape"""
    
    print("\n🔄 Testing alternative job sites...")
    
    # Alternative sites to test
    alternatives = [
        {
            'name': 'SimplyHired',
            'url': 'https://www.simplyhired.com/search?q=software+testing',
            'expected_elements': ['job', 'title']
        },
        {
            'name': 'Glassdoor',
            'url': 'https://www.glassdoor.com/Job/software-testing-jobs-SRCH_KO0,16.htm',
            'expected_elements': ['job', 'title']
        }
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    for site in alternatives:
        try:
            print(f"\n🌐 Testing {site['name']}: {site['url']}")
            
            response = requests.get(site['url'], headers=headers, timeout=10)
            print(f"  📊 Status: {response.status_code}")
            
            if response.status_code == 200:
                print(f"  📄 Page size: {len(response.content)} bytes")
                print(f"  ✅ {site['name']} accessible!")
                
                # Basic content check
                soup = BeautifulSoup(response.content, 'html.parser')
                job_related = soup.find_all(string=lambda x: x and any(word in x.lower() for word in ['engineer', 'developer', 'testing', 'qa']))[:3]
                
                if job_related:
                    print(f"  📋 Found job-related content:")
                    for content in job_related:
                        print(f"    - {content.strip()[:60]}...")
            else:
                print(f"  ❌ Status: {response.status_code}")
                
        except Exception as e:
            print(f"  ❌ Error accessing {site['name']}: {str(e)[:50]}...")

def main():
    print("🧪 Indeed Access Testing")
    print("=" * 50)
    
    # Test Indeed access
    success, working_url, working_headers = test_indeed_access()
    
    if success:
        print(f"\n✅ Found working configuration!")
        print(f"URL: {working_url}")
        print("Headers configured successfully")
    else:
        print("\n❌ No working Indeed configuration found")
        print("This is likely due to Indeed's anti-bot measures")
        
        # Test alternatives
        test_alternative_job_sites()
    
    print("\n💡 Recommendations:")
    print("1. Indeed actively blocks automated requests")
    print("2. Consider using Indeed's RSS feeds (if available)")
    print("3. Use official APIs when possible")
    print("4. Alternative: LinkedIn Jobs API, GitHub Jobs, or other job boards")
    print("5. For production: Consider using proxy services or browser automation")

if __name__ == "__main__":
    main()
