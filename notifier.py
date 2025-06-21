import smtplib
from email.message import EmailMessage
import os

def send_sms_via_email(subject, sender, to_sms_email):
    msg = EmailMessage()                                                    # creates email
    msg.set_content(f"Important email from {sender}\nSubject: {subject}")
    msg["From"] = os.getenv("ALERT_EMAIL")
    msg["To"] = to_sms_email
    msg["Subject"] = "New Important Email"

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:                       # connect to Gmail's SMTP server, logs in, and sends message to phone as text
        smtp.login(os.getenv("ALERT_EMAIL"), os.getenv("EMAIL_APP_PASSWORD"))
        smtp.send_message(msg)