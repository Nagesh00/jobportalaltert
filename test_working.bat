@echo off
echo 🚀 STARTING WORKING JOB MONITOR
echo ==============================

cd /d "%~dp0"

echo 📂 Current directory: %CD%
echo 🐍 Activating Python environment...

call .venv\Scripts\activate.bat

echo ✅ Environment activated
echo 🔍 Testing basic functionality...

python -c "import requests; print('✅ Requests module working')"
python -c "import datetime; print('✅ DateTime working')"
python -c "print('✅ Python is ready!')"

echo 📱 Testing Telegram connection...
python -c "
import requests
import datetime
try:
    telegram_config = {
        'bot_token': '8305949318:AAF257TSUv4EObGWLAAi7Cq7K87iambC9EM',
        'chat_id': '6411380646'
    }
    message = f'🧪 TEST from Windows at {datetime.datetime.now().strftime(\"%%H:%%M:%%S\")}'
    url = f'https://api.telegram.org/bot{telegram_config[\"bot_token\"]}/sendMessage'
    data = {'chat_id': telegram_config['chat_id'], 'text': message}
    response = requests.post(url, data=data, timeout=10)
    if response.status_code == 200:
        print('✅ Telegram test successful!')
    else:
        print(f'❌ Telegram failed: {response.status_code}')
except Exception as e:
    print(f'❌ Error: {e}')
"

echo 🔍 Testing RemoteOK API...
python -c "
import requests
try:
    url = 'https://remoteok.io/api'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    response = requests.get(url, headers=headers, timeout=15)
    if response.status_code == 200:
        jobs_data = response.json()
        job_count = len(jobs_data) - 1 if isinstance(jobs_data, list) and len(jobs_data) > 1 else 0
        print(f'✅ RemoteOK API working! Found {job_count} jobs')
    else:
        print(f'❌ RemoteOK failed: {response.status_code}')
except Exception as e:
    print(f'❌ RemoteOK error: {e}')
"

echo 🎯 Running GitHub Monitor Test...
python github_monitor.py

echo ✅ TEST COMPLETE!
pause
