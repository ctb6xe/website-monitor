#!/usr/bin/env python3
"""
Website Monitor - GitHub Actions Version
Monitors: https://www.thebestelectrolytepowders.com/
Runs: Daily at 8:30 AM EST via GitHub Actions
"""

import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import sys
import os

# Configuration from environment variables (set in GitHub Secrets)
TARGET_URL = os.environ.get('TARGET_URL', 'https://www.thebestelectrolytepowders.com/')
SENDER_EMAIL = os.environ.get('SENDER_EMAIL')
SENDER_PASSWORD = os.environ.get('SENDER_PASSWORD')
RECIPIENT_EMAIL = os.environ.get('RECIPIENT_EMAIL')
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

def check_website_status(url):
    """Check if website is accessible"""
    try:
        response = requests.get(url, timeout=10, allow_redirects=True)
        return True, response.status_code, None
    except requests.exceptions.RequestException as e:
        return False, None, str(e)

def send_email(subject, body):
    """Send email notification"""
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECIPIENT_EMAIL
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        
        print(f"✓ Email sent successfully to {RECIPIENT_EMAIL}")
        return True
    except Exception as e:
        print(f"✗ Failed to send email: {e}")
        return False

def main():
    print(f"\n{'='*60}")
    print(f"Website Monitor - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}")
    print(f"Checking: {TARGET_URL}")
    
    is_up, status_code, error = check_website_status(TARGET_URL)
    
    if is_up:
        print(f"✗ Website is STILL UP (Status: {status_code})")
        subject = "BEP Submit DMCA"
        body = f"""DMCA Takedown Reminder

The following website is still accessible:

URL: {TARGET_URL}
Status: Online (HTTP {status_code})
Check Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Action Required:
Consider resubmitting your DMCA takedown notice.

---
Automated notification from GitHub Actions
"""
        send_email(subject, body)
        return 1
    else:
        print(f"✓ Website is DOWN or inaccessible")
        if error:
            print(f"  Reason: {error}")
        subject = "BEP No DMCA Needed"
        body = f"""Good news! The website appears to have been taken down.

URL: {TARGET_URL}
Status: No longer accessible
Check Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Your DMCA takedown may have been successful!

---
Automated notification from GitHub Actions
"""
        send_email(subject, body)
        return 0

if __name__ == "__main__":
    sys.exit(main())
