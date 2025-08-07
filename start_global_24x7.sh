#!/bin/bash
echo "==============================================="
echo "    24/7 GLOBAL REAL-TIME JOB MONITORING"
echo "==============================================="
echo ""
echo "Starting worldwide job monitoring for software testing positions (2+ years)"
echo "Target email: kalyogyogi@gmail.com"
echo "Scan frequency: Every 90 seconds"
echo ""

cd "c:/Users/Nagnath/jobportal"

# Set environment variables if not already set
export TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN:-"8305949318:AAF257TSUv4EObGWLAAi7Cq7K87iambC9EM"}
export TELEGRAM_CHAT_ID=${TELEGRAM_CHAT_ID:-"6411380646"}

echo "Telegram Bot: ${TELEGRAM_BOT_TOKEN:0:20}..."
echo "Chat ID: $TELEGRAM_CHAT_ID"
echo ""

echo "Starting 24/7 monitoring..."
echo "Press Ctrl+C to stop monitoring"
echo ""

python global_24x7_realtime_monitor.py
