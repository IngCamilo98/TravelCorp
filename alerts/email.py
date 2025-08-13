import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email_raw(sender: str, password: str, recipient: str, subject: str, body: str):
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender, password)
        server.sendmail(sender, recipient, msg.as_string())

def send_email(recipient: str, subject: str, body: str):
    sender = os.environ.get('EMAIL_ADDRESS')
    password = os.environ.get('EMAIL_APP_PASSWORD')
    if not sender or not password:
        raise ValueError('EMAIL_ADDRESS y EMAIL_APP_PASSWORD deben estar definidos en las variables de entorno.')
    send_email_raw(sender, password, recipient, subject, body)
