#!/bin/bash

# REAL-TIME Job Monitoring Startup Script for Linux/Mac
echo "🚨 STARTING REAL-TIME JOB MONITORING 🚨"
echo "======================================"
echo ""
echo "Your bot will scan for NEW testing jobs every 2 minutes"
echo "and send INSTANT Telegram alerts!"
echo ""
echo "Press Ctrl+C to stop monitoring"
echo ""

# Set environment variables
export TELEGRAM_BOT_TOKEN="8305949318:AAF257TSUv4EObGWLAAi7Cq7K87iambC9EM"
export TELEGRAM_CHAT_ID="6411380646"
export SENDER_EMAIL="kalyogyogi@gmail.com"
export RECIPIENT_EMAIL="kalyogyogi@gmail.com"

# Start the enhanced real-time monitor
python3 enhanced_realtime_monitor.py
