import imaplib, email
from email.header import decode_header

def fetch_unread_emails(account, important_keywords):
    imap = imaplib.IMAP4_SSL(account['imap'])
    imap.login(account['email'],account['password'])
    imap.select("inbox")
    status, messages = imap.search(None, '(UNSEEN)')
    emails = []

    for num in messages[0].split():
        _, data = imap.fetch(num, "(RFC822)")
        msg = email.message_from_bytes(data[0][1])
        subject, _ = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode()
        sender = msg.get("From")
        if any(k.lower() in subject.lower() for k in important_keywords):
            emails.append({"subject": subject, "sender": sender})

    imap.logout()
    return emails