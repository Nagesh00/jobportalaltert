#!/bin/bash

echo "🚨 STARTING 24/7 GLOBAL SOFTWARE TESTING JOB MONITOR 🚨"
echo ""
echo "🎯 Target: Software Testing Jobs (2+ Years Experience)"
echo "🌍 Coverage: Indeed Global + RemoteOK + WeWorkRemotely + More"
echo "📱 Alerts: IMMEDIATE Telegram notifications"
echo "⏱️  Frequency: Every 90 seconds (24/7)"
echo ""

# Set environment variables for Telegram
export TELEGRAM_BOT_TOKEN="8305949318:AAF257TSUv4EObGWLAAi7Cq7K87iambC9EM"
export TELEGRAM_CHAT_ID="6411380646"

# Optional: Set email password if you want email alerts too
# export EMAIL_APP_PASSWORD="your_gmail_app_password_here"

echo "🔧 Environment configured"
echo "📱 Telegram Bot: READY"
echo "🌍 Global job sources: READY"
echo ""

echo "🚀 Launching 24/7 monitoring..."
echo "⚠️  Press Ctrl+C to stop monitoring"
echo ""

python3 global_24x7_monitor.py

echo ""
echo "⏹️  24/7 monitoring stopped"
