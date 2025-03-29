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
def send_email(content_msg):
    message = EmailMessage()
    message["From"] = EMAIL_ACCOUNT
    message["To"] = RECIPIENT
    message["Subject"] = "Temperature Control"
    # message.set_content(f"The current temperature is {TEMP}°C. Would you like to turn the fan on?\n\n"
    #                     f"Please reply with 'YES' or 'NO'.")
   


    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>O'Block Automated Alerts</title>
    <style>
        :root {{
            --bg-color: #0a192f;
            --btn-bg: #000;
            --btn-hover-bg: linear-gradient(90deg, #233554, #112240);
            --btn-hover-text: #64ffda;
            --btn-text: #eee;
        }}
       
        body,
        table,
        td,
        p,
        a,
        div {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}


        body {{
            -webkit-text-size-adjust: none;
            -ms-text-size-adjust: none;
            background-color: #0d1b2a;
            color: #e0e0e0;
            font-family: 'Helvetica', Arial, sans-serif;
        }}


        a {{
            color: #ff4757;
            text-decoration: none;
        }}


        .container {{
            width: 100%;
            max-width: 600px;
            margin: 0 auto;
            background-color: #1b263b;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.4);
            margin-top: 20px;
        }}


        .content {{
            padding: 20px;
            text-align: center;
        }}


        .warning-banner {{
            background-color: #000;
            color: #fff;
            padding: 12px;
            font-weight: bold;
            border-radius: 4px 4px 0 0;
            margin-bottom: 15px;
        }}


        .warning-banner i {{
            margin-right: 8px;
            margin-left: 8px;
            font-size: 18px;
            color: yellow;
        }}


        .content p {{
            font-size: 15px;
            line-height: 1.6;
            margin-bottom: 20px;
            color: #d3d3d3;
        }}


        .temp-value {{
            font-size: 17px;
            color: #ff4757;
        }}


        .action-button {{
            margin-top: 15px;
            padding: 10px 24px;
            font-size: 14px;
            font-weight: bold;
            color: var(--btn-text);
            background-color: var(--btn-bg);
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: background 0.3s, transform 0.2s, color 0.3s;
        }}


        .action-button:hover {{
            background: var(--btn-hover-bg);
            color: var(--btn-hover-text);
            transform: scale(1.05);
        }}


        .ignore:hover {{
            text-decoration: line-through;
        }}


        .automated {{
            font-size: 10.5px;
            display: flex;
            justify-content: end;
            color: rgb(122, 120, 122);
            font-style: italic;
            font-weight: bold;
        }}


        @media only screen and (max-width: 600px) {{
            .container {{
                width: 100% !important;
            }}
            .action-button {{
                display: block;
                margin: 10px auto;
                width: 80%;
            }}
        }}
    </style>
</head>
<body>
    <table class="container" cellpadding="0" cellspacing="0" border="0">
        <tr>
            <td class="content">
                <div class="warning-banner">
                    <span style="color: yellow;">&#9888; &nbsp;</span>
                    Alert: Elevated Temperature Detected
                    &nbsp;<span style="color: yellow;">&#9888;</span>
                </div>
                <p>
                    The current temperature is <span class="temp-value">{content_msg}</span>.
                </p>
                <a href="mailto:{EMAIL_ACCOUNT}?subject=Temperature%20Response&body=YES" class="action-button">
                    Activate Fan
                </a>
                <a href="mailto:{EMAIL_ACCOUNT}?subject=Temperature%20Response&body=NO"
                   class="ignore"
                   style="display: block; color: #a9a9a9; margin-top: 20px;">
                    Ignore
                </a>
                <span class="automated">O'Blocks Automated Messages</span>
            </td>
        </tr>
    </table>
</body>
</html>"""
   
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
                                body = part.get_payload(decode=True).decode().strip().upper()
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
                        mail.store(notification, '+FLAGS', '\\Seen')
                        mail.logout()
                        return None
        mail.logout()
        return None
   
    except Exception as e:
        print(f"Error Receiving Emails: {e}")
        return None