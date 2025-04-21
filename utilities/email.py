#!/usr/bin/env python3
""" Email service for Expense Tracker """

import base64
from datetime import datetime
from os import getenv
from utilities.statement import Statement
import yagmail
from yagmail.error import YagInvalidEmailAddress, YagAddressError
import re
from smtplib import SMTPConnectError, SMTPServerDisconnected
from typing import Dict, Literal


X_username = getenv('X_USERNAME', "AIIkpenyi")
IG_username = getenv('IG_USERNAME', "ifeanyianthony")


def _get_default_user() -> set:
    """ Helper function to return Default Mail details """
    from api.v1.app import app

    dev_email = app.config['MAIL_DEFAULT_SENDER']
    dev_password = app.config['MAIL_PASSWORD']

    if not dev_email or not dev_password:
        print('Email/Password not found in the .env file')
        exit(1)

    return dev_email, dev_password


def get_logo_b64(path: str = "static/images/logo.png") -> str:
    """ Returns the B64 version of the logo """
    with open(path, 'rb') as img:
        enc_img = base64.b64encode(img.read()).decode('utf-8')

    return enc_img


class Email:
    """ Defining the Email class """

    @classmethod
    def send_confirmation_email(self, user, OTP: int, OTP_TIMEOUT: int) -> bool:
        """ Sends a confirmation email with token """
        if user and OTP_TIMEOUT:
            dev_email, dev_password = _get_default_user()

            connect = yagmail.SMTP(dev_email, dev_password)

            subject = "Welcome to Expense Tracker!"
            content = f"""
            <html>
            <body style="font-family: Arial, sans-serif; background-color: #f5f5f5; color: #333; margin: 0; padding: 20px;">
                <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
                    <div style="background-color: #4CAF50; color: #ffffff; padding: 10px; text-align: center; border-radius: 10px 10px 0 0;">
                        <img src="data:image/png;base64,{get_logo_b64()}" alt="Expense Tracker Logo" style="width: 150px; height: auto;">
                    </div>
                    <div style="padding: 20px;">
                        <p style="font-size: 16px; line-height: 1.6; margin: 10px 0;">Dear {user.first_name} {user.last_name},</p>
                        <p style="font-size: 16px; line-height: 1.6; margin: 10px 0;">Thank you for registering with Expense Tracker! To complete your registration and gain access to this site, please verify your email address using the OTP below:</p>

                        <div style="display: inline-block; background-color: #4CAF50; color: #ffffff; text-decoration: none; padding: 10px 20px; border-radius: 10px; align-items: center;">
                            <h3 style="font-size: 22px; text-align: center;">{OTP}</h2>
                        </div>

                        <p style="font-size: 16px; line-height: 1.6; margin: 10px 0;">If you have any questions or need assistance, feel free to reach out to us.</p>
                        <a href="http://127.0.0.1:5000/support" style="display: inline-block; background-color: #4CAF50; color: #ffffff; text-decoration: none; padding: 10px 20px; border-radius: 5px; margin-top: 20px; font-size: 16px;">Contact Support</a>
                        <p style="font-style: italic; color: #555; font-size: 14px; line-height: 1.6; margin: 20px 0;">
                            Kindly note that the OTP expires after {OTP_TIMEOUT} minutes.
                        </p>
                    </div>
                    <div style="text-align: center;">
                        <table align="center" style="margin: 0 auto;">
                            <tr>
                                <td style="padding: 0 5px;">
                                    <a href="https://x.com/{X_username}" target="_blank">
                                        <img src="https://upload.wikimedia.org/wikipedia/commons/c/ce/X_logo_2023.svg" alt="X logo" width="20" style="display: block;"/>
                                    </a>
                                </td>
                                <td style="padding: 0 5px;">
                                    <a href="https://instagram.com/{IG_username}" target="_blank">
                                        <img src="https://upload.wikimedia.org/wikipedia/commons/a/ac/Instagram-Gradient-Logo-PNG.png" alt="Instagram logo" width="20" style="display: block;"/>
                                    </a>
                                </td>
                            </tr>
                        </table>
                    </div>
                    <div style="text-align: center; font-size: 12px; color: #888; padding: 10px; border-top: 1px solid #ddd;">
                        &copy; {datetime.now().year} Expense Tracker. All rights reserved.
                    </div>
                </div>
            </body>
            </html>
            """

            # Minify the HTML content to reduce whitespace
            content = re.sub(r'\s+', ' ', content.strip())

            try:
                connect.send(user.email, subject=subject, contents=content)
                connect.close()
                return True
            except (YagAddressError, YagInvalidEmailAddress):
                pass

        return False

    @classmethod
    def send_otp(self, user, OTP: int, OTP_TIMEOUT: int) -> bool:
        """ Sends a confirmation email with token """
        if user and OTP_TIMEOUT:
            dev_email, dev_password = _get_default_user()
            connect = yagmail.SMTP(dev_email, dev_password)

            subject = "OTP | Expense Tracker"
            content = f"""
            <html>
            <body style="font-family: Arial, sans-serif; background-color: #f5f5f5; color: #333; margin: 0; padding: 20px;">
                <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
                    <div style="background-color: transparent; padding: 10px; text-align: center; border-radius: 10px 10px 0 0;">
                        <img src="data:image/png;base64,{get_logo_b64()}" alt="Expense Tracker Logo" style="width: 150px; height: auto;">
                    </div>
                    <div style="padding: 20px;">
                        <p style="font-size: 16px; line-height: 1.6; margin: 10px 0;">Dear {user.first_name} {user.last_name},</p>
                        <p style="font-size: 16px; line-height: 1.6; margin: 10px 0;">Please authenticate the session using the OTP below:</p>

                        <div style="display: inline-block; background-color: #4CAF50; color: #ffffff; text-decoration: none; padding: 10px 20px; border-radius: 10px; align-items: center;">
                            <h3 style="font-size: 22px; text-align: center;">{OTP}</h2>
                        </div>

                        <p style="font-size: 16px; line-height: 1.6; margin: 10px 0;">If you have any questions or need assistance, feel free to reach out to us.</p>
                        <a href="http://127.0.0.1:5000/support" style="display: inline-block; background-color: #4CAF50; color: #ffffff; text-decoration: none; padding: 10px 20px; border-radius: 10px; margin-top: 20px; font-size: 16px;">Contact Support</a>
                        <p style="font-style: italic; color: #555; font-size: 14px; line-height: 1.6; margin: 20px 0;">
                            Kindly note that the OTP expires after {OTP_TIMEOUT} minutes.
                        </p>
                        <p style="font-style: italic; color: #555; font-size: 14px; line-height: 1.6; margin: 20px 0;">
                            If you did not initiate this request, please ignore and proceed to change your password.
                        </p>
                    </div>
                    <div style="text-align: center;">
                        <table align="center" style="margin: 0 auto;">
                            <tr>
                                <td style="padding: 0 5px;">
                                    <a href="https://x.com/{X_username}" target="_blank">
                                        <img src="https://upload.wikimedia.org/wikipedia/commons/c/ce/X_logo_2023.svg" alt="X logo" width="20" style="display: block;"/>
                                    </a>
                                </td>
                                <td style="padding: 0 5px;">
                                    <a href="https://instagram.com/{IG_username}" target="_blank">
                                        <img src="https://upload.wikimedia.org/wikipedia/commons/a/ac/Instagram-Gradient-Logo-PNG.png" alt="Instagram logo" width="20" style="display: block;"/>
                                    </a>
                                </td>
                            </tr>
                        </table>
                    </div>
                    <div style="text-align: center; font-size: 12px; color: #888; padding: 10px; border-top: 1px solid #ddd;">
                        &copy; {datetime.now().year} Expense Tracker. All rights reserved.
                    </div>
                </div>
            </body>
            </html>
            """

            # Minify the HTML content to reduce whitespace
            content = re.sub(r'\s+', ' ', content.strip())

            try:
                connect.send(user.email, subject=subject, contents=content)
                connect.close()
                return True
            except (YagAddressError, YagInvalidEmailAddress):
                pass

        return False

    @classmethod
    def send_statement(self, user, period: Dict[str, str],
                       send_as: Literal['xlsx', 'pdf'] = 'xlsx') -> bool:
        """ Sends the user's full statement to the registered email """
        if not user:
            return False

        dev_email, dev_password = _get_default_user()
        connect = yagmail.SMTP(dev_email, dev_password)

        Statement.prepare_statement(user, period, send_as)

        subject = "Your statement is ready!"

        content = f"""
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f5f5f5;
                    color: #333;
                    margin: 0;
                    padding: 20px;
                }}
                .email-container {{
                    max-width: 600px;
                    margin: 0 auto;
                    background-color: #ffffff;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                }}
                .header {{
                    background-color: transparent;
                    color: #ffffff;
                    padding: 10px;
                    text-align: center;
                    border-radius: 10px 10px 0 0;
                }}
                .content {{
                    padding: 20px;
                }}
                .content p {{
                    font-size: 16px;
                    line-height: 1.6;
                    margin: 10px 0;
                }}
                .footer {{
                    text-align: center;
                    font-size: 12px;
                    color: #888;
                    padding: 10px;
                    border-top: 1px solid #ddd;
                }}
                .button {{
                    display: inline-block;
                    background-color: #4CAF50;
                    color: #ffffff;
                    text-decoration: none;
                    padding: 10px 20px;
                    border-radius: 5px;
                    margin-top: 20px;
                }}
                .italic {{
                    font-style: italic;
                    color: #555;
                }}
            </style>
        </head>
        <body>
            <div class="email-container">
                <div class="header">
                    <img src="data:image/png;base64,{get_logo_b64()}" alt="Expense Tracker Logo" style="width: 150px; height: auto;">
                </div>
                <div class="content">
                    <p>Dear {user.first_name},</p>
                    <p>We are pleased to inform you that your expense statement has been successfully generated. You can now review your detailed expense report.</p>
                    <p>Please find the attached statement.</p>
                    <p>If you have any questions or need assistance, feel free to reach out to us.</p>
                    <a href="http://127.0.0.1:5000/support" class="button">Contact Support</a>
                    <p class="italic">
                        If you did not request this statement, please reset your password or contact our support team for further assistance.
                    </p>
                </div>
                <div style="text-align: center; margin-top: 10px;">
                    <table align="center" style="margin: 0 auto;">
                        <tr>
                            <td style="padding: 0 5px;">
                                <a href="https://x.com/{X_username}" target="_blank">
                                    <img src="https://upload.wikimedia.org/wikipedia/commons/c/ce/X_logo_2023.svg" alt="X logo" width="20" style="display: block;"/>
                                </a>
                            </td>
                            <td style="padding: 0 5px;">
                                <a href="https://instagram.com/{IG_username}" target="_blank">
                                    <img src="https://upload.wikimedia.org/wikipedia/commons/a/ac/Instagram-Gradient-Logo-PNG.png" alt="Instagram logo" width="20" style="display: block;"/>
                                </a>
                            </td>
                        </tr>
                    </table>
                </div>
                <div class="footer">
                    &copy; {datetime.now().year} Expense Tracker. All rights reserved.
                </div>
            </div>
        </body>
        </html>
        """

        # Minify the HTML content to reduce whitespace
        content = re.sub(r'\s+', ' ', content.strip())

        try:
            connect.send(user.email, subject=subject, contents=content, attachments=['statement.xlsx'])
            connect.close()
            return True
        except (YagAddressError,
                YagInvalidEmailAddress,
                SMTPConnectError,
                SMTPServerDisconnected):
            return False
