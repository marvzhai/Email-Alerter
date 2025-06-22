from twilio.rest import Client
import os
from dotenv import load_dotenv
load_dotenv()

def send_sms_via_twilio(subject, sender):
    try:
        print("[*] Sending SMS...")  # Confirm function is called

        client = Client(os.getenv("TWILIO_SID"), os.getenv("TWILIO_AUTH_TOKEN"))

        body = f"Important email from {sender}\nSubject: {subject}"
        body = body[:160]

        message = client.messages.create(
            body=body,
            from_=os.getenv("TWILIO_FROM_NUMBER"),
            to=os.getenv("TO_PHONE_NUMBER")
        )

        print(f"[+] Sent SMS: {message.sid}")
    except Exception as e:
        print(f"[!] Error sending SMS: {e}")
