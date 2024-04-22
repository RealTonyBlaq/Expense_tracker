#!/usr/bin/python3


import smtplib
from email.message import EmailMessage
from ssl import create_default_context
import json
import os


def send_email():
    """ Set up the email message """
    msg = EmailMessage()
    msg['Subject'] = 'Third Test Email'
    msg['From'] = 'ifeanyiikpenyi@yahoo.com'
    msg['To'] = 'ifeanyi3797@gmail.com'
    msg.set_content('<h1 style="color: blue;">This is an HTML email content</h1>')
    #msg.add_alternative('<h1 style="color: blue;">This is an HTML email content</h1>')

    # Set up the SMTP connection
    smtp_server = 'smtp.mail.yahoo.com'
    smtp_port = 465

    try:
        with open('credentials.json') as f:
            credentials = json.load(f)
        username = credentials['username']
        password = credentials['password']
    except FileNotFoundError as mess:
        print(mess)

    try:
        """ Establish a secure connection with the SMTP server """
        context = create_default_context()
        with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
            server.login(username, password)
            server.send_message(msg)
        print('Email sent successfully!')
    except Exception as e:
        print(f'Error sending email: {str(e)}')

# Call the function to send the email
send_email()
