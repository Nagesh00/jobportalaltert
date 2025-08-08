#!/usr/bin/env python3
"""
Jooble API Test
Test the new Jooble integration for worldwide job coverage
"""

import requests
import json
import datetime

def test_jooble_api():
    print("🌍 TESTING JOOBLE API")
    print("=" * 40)
    print(f"⏰ Time: {datetime.datetime.now().strftime('%H:%M:%S')}")
    
    # Jooble API configuration
    api_key = '4452241a-50c6-416b-a47a-98261c93fd39'
    base_url = f"https://jooble.org/api/{api_key}"
    
    # Test 1: Basic API connection
    def test_basic_connection():
        try:
            search_params = {
                'keywords': 'software testing',
                'location': '',
                'page': '1'
            }
            
            headers = {
                'Content-Type': 'application/json',
                'User-Agent': 'JobMonitor/1.0'
            }
            
            response = requests.post(base_url, json=search_params, headers=headers, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                total_results = data.get('totalCount', 0)
                jobs = data.get('jobs', [])
                
                print(f"✅ Jooble API Connected!")
                print(f"📊 Total testing jobs available: {total_results}")
                print(f"🎯 Sample jobs retrieved: {len(jobs)}")
                
                return True, jobs
            else:
                print(f"❌ Jooble API failed: {response.status_code}")
                print(f"Response: {response.text[:200]}")
                return False, []
                
        except Exception as e:
            print(f"❌ Jooble API error: {str(e)}")
            return False, []
    
    # Test 2: Advanced testing job search
    def test_advanced_search():
        try:
            search_params = {
                'keywords': 'software testing QA automation test engineer',
                'location': '',
                'page': '1'
            }
            
            headers = {'Content-Type': 'application/json'}
            response = requests.post(base_url, json=search_params, headers=headers, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                jobs = data.get('jobs', [])
                
                quality_jobs = []
                for job in jobs[:10]:  # Check first 10 jobs
                    title = str(job.get('title', '')).lower()
                    snippet = str(job.get('snippet', '')).lower()
                    
                    # Check for testing keywords
                    testing_keywords = ['test', 'qa', 'quality', 'automation', 'selenium']
                    has_testing = any(keyword in title or keyword in snippet for keyword in testing_keywords)
                    
                    # Check for experience
                    exp_keywords = ['2+ year', 'experienced', 'senior', 'experience']
                    has_experience = any(keyword in snippet for keyword in exp_keywords)
                    
                    if has_testing and has_experience:
                        quality_jobs.append({
                            'title': job.get('title'),
                            'company': job.get('company'),
                            'location': job.get('location'),
                            'salary': job.get('salary', 'Competitive'),
                            'link': job.get('link'),
                            'snippet': snippet[:100] + '...'
                        })
                
                print(f"🎯 Quality testing jobs found: {len(quality_jobs)}")
                
                # Show sample jobs
                for i, job in enumerate(quality_jobs[:3], 1):
                    print(f"\n📝 Job {i}:")
                    print(f"   Title: {job['title']}")
                    print(f"   Company: {job['company']}")
                    print(f"   Location: {job['location']}")
                    print(f"   Salary: {job['salary']}")
                    print(f"   Preview: {job['snippet']}")
                
                return len(quality_jobs) > 0
            else:
                print(f"❌ Advanced search failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Advanced search error: {str(e)}")
            return False
    
    # Test 3: Global coverage test
    def test_global_coverage():
        try:
            locations = ['London', 'New York', 'Berlin', 'Sydney', 'Toronto']
            global_results = {}
            
            for location in locations:
                search_params = {
                    'keywords': 'software testing',
                    'location': location,
                    'page': '1'
                }
                
                response = requests.post(base_url, json=search_params, headers={'Content-Type': 'application/json'}, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    job_count = len(data.get('jobs', []))
                    global_results[location] = job_count
                else:
                    global_results[location] = 0
            
            print(f"\n🌍 Global Coverage Test:")
            total_global = 0
            for location, count in global_results.items():
                print(f"   {location}: {count} jobs")
                total_global += count
            
            print(f"📊 Total global jobs: {total_global}")
            return total_global > 0
            
        except Exception as e:
            print(f"❌ Global coverage error: {str(e)}")
            return False
    
    # Test 4: Telegram alert test
    def test_telegram_with_jooble():
        try:
            bot_token = '8305949318:AAF257TSUv4EObGWLAAi7Cq7K87iambC9EM'
            chat_id = '6411380646'
            
            message = f"🌍 **JOOBLE INTEGRATION TEST** 🌍\n\n"
            message += f"✅ Jooble API is now integrated!\n"
            message += f"⏰ Time: {datetime.datetime.now().strftime('%H:%M:%S')}\n"
            message += f"🎯 Now monitoring worldwide jobs!\n"
            message += f"🚀 5 job sources active:\n"
            message += f"   • RemoteOK\n"
            message += f"   • Stack Overflow\n"
            message += f"   • Indeed\n"
            message += f"   • Reed.co.uk\n"
            message += f"   • Jooble (NEW!)\n\n"
            message += f"🌐 **Global job aggregation activated!**"
            
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            data = {'chat_id': chat_id, 'text': message, 'parse_mode': 'Markdown'}
            
            response = requests.post(url, data=data, timeout=10)
            return response.status_code == 200
            
        except:
            return False
    
    # Run all tests
    print(f"\n🔧 RUNNING JOOBLE API TESTS:")
    
    # Test 1
    api_ok, sample_jobs = test_basic_connection()
    
    # Test 2
    advanced_ok = test_advanced_search() if api_ok else False
    
    # Test 3
    global_ok = test_global_coverage() if api_ok else False
    
    # Test 4
    telegram_ok = test_telegram_with_jooble()
    
    print(f"\n📊 TEST RESULTS:")
    print(f"🌐 Jooble API: {'✅ WORKING' if api_ok else '❌ FAILED'}")
    print(f"🎯 Advanced Search: {'✅ WORKING' if advanced_ok else '❌ FAILED'}")
    print(f"🌍 Global Coverage: {'✅ WORKING' if global_ok else '❌ FAILED'}")
    print(f"📱 Telegram: {'✅ SENT' if telegram_ok else '❌ FAILED'}")
    
    if api_ok and advanced_ok:
        print(f"\n🎉 JOOBLE INTEGRATION SUCCESS!")
        print(f"✅ Your monitor now has MASSIVE worldwide coverage!")
        print(f"🌍 Jooble aggregates jobs from thousands of websites")
        print(f"💼 Excellent for finding jobs in any location")
        print(f"📈 Significantly increased job discovery")
        print(f"\n🚀 Total job sources now: 5")
        print(f"   📊 Unprecedented job coverage!")
        
        return True
    else:
        print(f"\n⚠️ INTEGRATION ISSUES:")
        if not api_ok:
            print(f"   • Check Jooble API key")
        if not advanced_ok:
            print(f"   • Advanced search needs adjustment")
        
        return False

if __name__ == "__main__":
    test_jooble_api()
