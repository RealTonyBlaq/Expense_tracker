#!/usr/bin/python3
""" Email Service """

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.auth.transport import requests
from google.oauth2 import service_account


credentials = service_account.Credentials.from_service_account_file('credentials.json')
# Email configuration
sender_email = 'ifeanyi3797@gmail.com'
receiver_email = 'ifeanyiikpenyi@yahoo.com'
subject = 'Hello from Python!'
message = 'This is the body of the email.'

# SMTP server configuration
smtp_server = 'smtp.mail.yahoo.com'
smtp_port = 465

# Create a multipart message and set the headers
msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = receiver_email
msg['Subject'] = subject

# Attach the message to the MIMEMultipart object
msg.attach(MIMEText(message, 'plain'))

# Connect to the SMTP server and send the email
try:
    with smtplib.SMTP_SSL(smtp_server, smtp_port) as smtp_obj:
        smtp_obj.starttls()  # Enable TLS encryption
        smtp_obj.login(sender_email, 'ifeANYI8796')  # Replace with your email password

        # Send the email
        smtp_obj.sendmail(sender_email, receiver_email, msg.as_string())
        print('Email sent successfully!')
except smtplib.SMTPException as e:
    print('Error occurred while sending the email:', str(e))
