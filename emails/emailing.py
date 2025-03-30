import RPi.GPIO as GPIO  # type: ignore
import smtplib  # try doing sudo apt install python3-smtplib / or python3-secure-smtplib
import imaplib  # try doing sudo apt install python3-imaplib
import email
from email.message import EmailMessage
from jinja2 import Environment, FileSystemLoader
import os

# Setup Jinja2 Environment
template_dir = os.path.join(os.path.dirname(__file__), "..", "src", "Views")
env = Environment(loader=FileSystemLoader(template_dir))

# email infos
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
IMAP_SERVER = "imap.gmail.com"
IMAP_PORT = 993


EMAIL_ACCOUNT = "smartdashboard60@gmail.com"
EMAIL_PASSWORD = "koyu oxxd rdvj hxzl"
RECIPIENT = "nathanielbitton18@gmail.com"


fan_state = False


# sending email function
def send_email(content_msg, is_temp=True):
    message = EmailMessage()
    message["From"] = EMAIL_ACCOUNT
    message["To"] = RECIPIENT
    message["Subject"] = "Temperature Control" if is_temp else "Light Alert"

    # Render the email.html template with the dynamic variable
    template = env.get_template("email.html")
    html_content = template.render(
        value=content_msg, is_temp=is_temp, email_account=EMAIL_ACCOUNT
    )

    message.add_alternative(html_content, subtype="html")

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
        server.send_message(message)
        server.quit()
        print("You have a new email!")
    except Exception as e:
        print(f"Error Sending Email: {e}")


# checking the email response function
def check_response():
    global email_sent

    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
        mail.select("inbox")

        status, messages = mail.search(None, "Unseen")
        notifications = messages[0].split()

        if not notifications:
            print("You have no new emails.")
            return None

        for notification in notifications:
            status, message_data = mail.fetch(notification, "(RFC822)")
            for response_part in message_data:
                if isinstance(response_part, tuple):
                    message = email.message_from_bytes(response_part[1])
                    subject = message["subject"]
                    sender = message["from"]

                    # email body
                    if message.is_multipart():
                        for part in message.walk():
                            if part.get_content_type() == "text/plain":
                                body = (
                                    part.get_payload(decode=True)
                                    .decode()
                                    .strip()
                                    .upper()
                                )
                                break
                    else:
                        body = message.get_payload(decode=True).decode().strip().upper()

                    print(f"\nNew Email from {sender}")
                    print(f"Subject: {subject}")
                    print(f"Message:\n{body}")

                    # this is the fan status based on response of the user
                    first_word = body.strip().split()[0].upper()

                    if first_word == "YES":
                        print("Fan turned ON.")
                        email_sent = False
                        mail.logout()
                        return True
                    elif first_word == "NO":
                        print("Fan turned OFF.")
                        email_sent = False
                        mail.logout()
                        return False
                    else:
                        print("Invalid response in email body. Email Ignored.")
                        mail.store(notification, "+FLAGS", "\\Seen")
                        mail.logout()
                        return None
        mail.logout()
        return None

    except Exception as e:
        print(f"Error Receiving Emails: {e}")
        return None
