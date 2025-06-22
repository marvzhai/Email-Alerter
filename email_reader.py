import imaplib, email
from email.header import decode_header
from email.utils import parsedate_to_datetime
from datetime import datetime, timedelta, timezone

def fetch_unread_emails(account, important_keywords):
    imap = imaplib.IMAP4_SSL(account['imap'])
    imap.login(account['email'],account['password'])
    imap.select("inbox")

    print("[>] Connecting to IMAP...")
    imap = imaplib.IMAP4_SSL(account['imap'])

    print("[>] Logging in...")
    imap.login(account['email'], account['password'])

    print("[>] Selecting inbox...")
    imap.select("inbox")

    #get all unread emails today
    today = datetime.now().strftime("%d-%b-%Y")
    print("[>] Searching for unread emails...")
    status, messages = imap.search(None, f'(UNSEEN SINCE {today})')
    emails = []

    now = datetime.now(timezone.utc)
    four_hours_ago = now - timedelta(hours=4)

    for num in messages[0].split():
        _, data = imap.fetch(num, "(RFC822)")
        msg = email.message_from_bytes(data[0][1])

        subject, _ = decode_header(msg["Subject"])[0]
        
        if isinstance(subject, bytes):
            subject = subject.decode()

        sender = msg.get("From")

        date_header = msg.get("Date")
        if date_header:
            try:
                email_time = parsedate_to_datetime(date_header)
                if email_time < four_hours_ago or email_time > now:
                    continue  # Skip old or future emails
            except Exception as e:
                print(f"[!] Failed to parse date: {e}")
                continue

        if any(k.lower() in subject.lower() for k in important_keywords):
            emails.append({"subject": subject, "sender": sender})

    imap.logout()
    return emails