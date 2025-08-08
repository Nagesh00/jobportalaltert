#!/usr/bin/env python3
"""
Reed.co.uk API Test
Test the new Reed.co.uk integration
"""

import requests
import json
import datetime

def test_reed_api():
    print("🇬🇧 TESTING REED.CO.UK API")
    print("=" * 40)
    print(f"⏰ Time: {datetime.datetime.now().strftime('%H:%M:%S')}")
    
    # Reed API configuration
    api_key = 'a3109410-807f-4753-b098-353adb07a966'
    base_url = "https://www.reed.co.uk/api/1.0/search"
    
    # Test 1: Basic API connection
    def test_basic_connection():
        try:
            params = {
                'keywords': 'software testing',
                'resultsToTake': 5
            }
            
            auth = (api_key, '')
            headers = {'User-Agent': 'JobMonitor/1.0'}
            
            response = requests.get(base_url, params=params, auth=auth, headers=headers, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                total_results = data.get('totalResults', 0)
                jobs = data.get('results', [])
                
                print(f"✅ Reed API Connected!")
                print(f"📊 Total testing jobs available: {total_results}")
                print(f"🎯 Sample jobs retrieved: {len(jobs)}")
                
                return True, jobs
            else:
                print(f"❌ Reed API failed: {response.status_code}")
                return False, []
                
        except Exception as e:
            print(f"❌ Reed API error: {str(e)}")
            return False, []
    
    # Test 2: Quality testing jobs
    def test_quality_jobs():
        try:
            params = {
                'keywords': 'software testing OR qa automation OR test engineer',
                'locationName': '',
                'resultsToTake': 10
            }
            
            auth = (api_key, '')
            response = requests.get(base_url, params=params, auth=auth, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                jobs = data.get('results', [])
                
                quality_jobs = []
                for job in jobs:
                    title = str(job.get('jobTitle', '')).lower()
                    description = str(job.get('jobDescription', '')).lower()
                    
                    # Check for testing keywords
                    testing_keywords = ['test', 'qa', 'quality', 'automation']
                    if any(keyword in title or keyword in description for keyword in testing_keywords):
                        # Check for experience
                        exp_keywords = ['2+ year', 'experienced', 'senior']
                        has_experience = any(keyword in description for keyword in exp_keywords)
                        
                        if has_experience:
                            quality_jobs.append({
                                'title': job.get('jobTitle'),
                                'company': job.get('employerName'),
                                'location': job.get('locationName'),
                                'salary': f"£{job.get('minimumSalary', 0):,} - £{job.get('maximumSalary', 0):,}",
                                'url': job.get('jobUrl')
                            })
                
                print(f"🎯 Quality testing jobs found: {len(quality_jobs)}")
                
                # Show sample jobs
                for i, job in enumerate(quality_jobs[:3], 1):
                    print(f"\n📝 Job {i}:")
                    print(f"   Title: {job['title']}")
                    print(f"   Company: {job['company']}")
                    print(f"   Location: {job['location']}")
                    print(f"   Salary: {job['salary']}")
                
                return len(quality_jobs) > 0
            else:
                print(f"❌ Quality job search failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Quality job error: {str(e)}")
            return False
    
    # Test 3: Telegram alert test
    def test_telegram_with_reed():
        try:
            bot_token = '8305949318:AAF257TSUv4EObGWLAAi7Cq7K87iambC9EM'
            chat_id = '6411380646'
            
            message = f"🇬🇧 **REED.CO.UK TEST** 🇬🇧\n\n"
            message += f"✅ Reed API is now integrated!\n"
            message += f"⏰ Time: {datetime.datetime.now().strftime('%H:%M:%S')}\n"
            message += f"🎯 Now monitoring UK jobs too!\n"
            message += f"🚀 4 job sources active:\n"
            message += f"   • RemoteOK\n"
            message += f"   • Stack Overflow\n"
            message += f"   • Indeed\n"
            message += f"   • Reed.co.uk (NEW!)"
            
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            data = {'chat_id': chat_id, 'text': message, 'parse_mode': 'Markdown'}
            
            response = requests.post(url, data=data, timeout=10)
            return response.status_code == 200
            
        except:
            return False
    
    # Run all tests
    print(f"\n🔧 RUNNING REED.CO.UK TESTS:")
    
    # Test 1
    api_ok, sample_jobs = test_basic_connection()
    
    # Test 2
    quality_ok = test_quality_jobs() if api_ok else False
    
    # Test 3
    telegram_ok = test_telegram_with_reed()
    
    print(f"\n📊 TEST RESULTS:")
    print(f"🌐 Reed API: {'✅ WORKING' if api_ok else '❌ FAILED'}")
    print(f"🎯 Quality Jobs: {'✅ FOUND' if quality_ok else '❌ NONE'}")
    print(f"📱 Telegram: {'✅ SENT' if telegram_ok else '❌ FAILED'}")
    
    if api_ok and quality_ok:
        print(f"\n🎉 REED.CO.UK INTEGRATION SUCCESS!")
        print(f"✅ Your monitor now covers UK jobs too!")
        print(f"🇬🇧 Reed.co.uk is one of the UK's largest job boards")
        print(f"💼 Excellent for UK-based testing positions")
        print(f"\n🚀 Total job sources now: 4")
        print(f"   📈 Significantly increased job coverage!")
        
        return True
    else:
        print(f"\n⚠️ INTEGRATION ISSUES:")
        if not api_ok:
            print(f"   • Check Reed API key")
        if not quality_ok:
            print(f"   • No quality jobs found (may be temporary)")
        
        return False

if __name__ == "__main__":
    test_reed_api()
