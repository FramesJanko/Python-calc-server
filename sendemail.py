import smtplib, ssl
from email.message import EmailMessage



def send_email(email_content="test text, is it working?"):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = 'joeysucks42069xx@gmail.com'  # Enter your address
    receiver_email = "rheckman4143@gmail.com"  # Enter receiver address
    password = 'fowo telh ipoh iqjy'
    text = email_content

    msg = EmailMessage()
    msg['Subject'] = "Flight Prices"
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg.set_content(text)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.send_message(msg)

