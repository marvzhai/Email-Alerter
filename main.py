from email_reader import fetch_unread_emails
from notifier import send_sms_via_twilio
import json, os
from dotenv import load_dotenv

load_dotenv()
print("TWILIO SID:", os.getenv("TWILIO_SID"))
print("TO_PHONE_NUMBER:", os.getenv("TO_PHONE_NUMBER"))

IMPORTANT_KEYWORDS = ["urgent", "interview", "offer", "action required", "*IMPORTANT*"]

def job():
    print("[*] Running job...")  # Confirm it's scheduled

    with open('config/accounts.json') as f:
        accounts = json.load(f)

    for account in accounts:
        print(f"[>] Checking {account['email']}")
        emails = fetch_unread_emails(account, IMPORTANT_KEYWORDS)
        print(f"[+] Found {len(emails)} important email(s).")

        for email in emails:
            print(f"[!] Sending alert for: {email['subject']}")
            send_sms_via_twilio(email['subject'], email['sender'])

job()