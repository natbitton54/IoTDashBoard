import RPi.GPIO as GPIO # type: ignore
import smtplib # try doing sudo apt install python3-smtplib / or python3-secure-smtplib
import imaplib # try doing sudo apt install python3-imaplib
import email
from email.message import EmailMessage

# email infos
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
IMAP_SERVER = "imap.gmail.com"
IMAP_PORT = 993

EMAIL_ACCOUNT = "smartdashboard60@gmail.com"
EMAIL_PASSWORD = "koyu oxxd rdvj hxzl"
RECIPIENT = "wayned0527@gmail.com"

fan_state = False

# sending email function
def send_email(TEMP):
    message = EmailMessage()
    message["From"] = EMAIL_ACCOUNT
    message["To"] = RECIPIENT
    message["Subject"] = "Temperature Control"
    message.set_content(f"The current temperature is {TEMP}°C. Would you like to turn the fan on?\n\n"
                        f"Please reply with 'YES' or 'NO'.")

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
        server.send_message(message)
        server.quit()
        print("Email Sent!")
    except Exception as e:
        print(f"Error Sending Email: {e}")

# checking the email response function
def check_response():
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
        mail.select("inbox")

        status, messages = mail.search(None, "Unseen")
        email_ids = messages[0].split()

        if not email_ids:
            print("No new emails.")
            return None

        for e_id in email_ids:
            status, message_data = mail.fetch(e_id, "(RFC822)")
            for response_part in message_data:
                if isinstance(response_part, tuple):
                    message = email.message_from_bytes(response_part[1])
                    subject = message["subject"]
                    sender = message["from"]

                    # email body
                    if message.is_multipart():
                        for part in message.walk():
                            if part.get_content_type() == "text/plain":
                                body = part.get_payload(decode=True).decode().strip().upper()
                                break
                    else:
                        body = message.get_payload(decode=True).decode().strip().upper()

                    print(f"\nNew Email from {sender}")
                    print(f"Subject: {subject}")
                    print(f"Message:\n{body}")

                    # this is the fan status based on response of the user
                    if "YES" in body:
                        print("Fan turned ON.")
                        mail.logout()
                        return True
                    elif "NO" in body:
                        print("Fan turned OFF.")
                        mail.logout()
                        return False
                    else:
                        print("Invalid response in email body. Email Ignored.")
                        mail.store(e_id, '+FLAGS', '\\Seen')
                        mail.logout()
                        return None
        mail.logout()
        return None
    
    except Exception as e:
        print(f"Error Receiving Emails: {e}")
        return None