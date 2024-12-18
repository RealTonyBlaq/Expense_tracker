#!/usr/bin/env python3
""" Email service for Expense Tracker """

from datetime import datetime
from utilities.statement import Statement
import yagmail
from yagmail.error import YagInvalidEmailAddress, YagAddressError
import re
from typing import Dict


def _get_default_user() -> list:
    """ Helper function to return Default Mail details """
    from api.v1.app import app

    dev_email = app.config['MAIL_DEFAULT_SENDER']
    dev_password = app.config['MAIL_PASSWORD']

    if not dev_email or not dev_password:
        print('Email/Password not found in the .env file')
        exit(1)

    return dev_email, dev_password


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
                        <h2 style="margin: 0; font-size: 24px;">Expense Tracker</h2>
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
                    <div style="text-align: center; font-size: 12px; color: #888; padding: 10px; border-top: 1px solid #ddd;">
                        &copy; {datetime.now().year} Expense Tracker. All rights reserved.
                    </div>
                </div>
            </body>
            </html>
            """

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
                    <div style="background-color: #4CAF50; color: #ffffff; padding: 10px; text-align: center; border-radius: 10px 10px 0 0;">
                        <h2 style="margin: 0; font-size: 24px;">Expense Tracker</h2>
                    </div>
                    <div style="padding: 20px;">
                        <p style="font-size: 16px; line-height: 1.6; margin: 10px 0;">Dear {user.first_name} {user.last_name},</p>
                        <p style="font-size: 16px; line-height: 1.6; margin: 10px 0;">Please authenticate the session using the OTP below:</p>

                        <div style="display: inline-block; background-color: #4CAF50; color: #ffffff; text-decoration: none; padding: 10px 20px; border-radius: 10px; align-items: center;">
                            <h3 style="font-size: 22px; text-align: center;">{OTP}</h2>
                        </div>

                        <p style="font-size: 16px; line-height: 1.6; margin: 10px 0;">If you have any questions or need assistance, feel free to reach out to us.</p>
                        <a href="http://127.0.0.1:5000/support" style="display: inline-block; background-color: #4CAF50; color: #ffffff; text-decoration: none; padding: 10px 20px; border-radius: 5px; margin-top: 20px; font-size: 16px;">Contact Support</a>
                        <p style="font-style: italic; color: #555; font-size: 14px; line-height: 1.6; margin: 20px 0;">
                            Kindly note that the OTP expires after {OTP_TIMEOUT} minutes.
                        </p>
                        <p style="font-style: italic; color: #555; font-size: 14px; line-height: 1.6; margin: 20px 0;">
                            If you did not initiate this request, please ignore and proceed to change your password.
                        </p>
                    </div>
                    <div style="text-align: center; font-size: 12px; color: #888; padding: 10px; border-top: 1px solid #ddd;">
                        &copy; {datetime.now().year} Expense Tracker. All rights reserved.
                    </div>
                </div>
            </body>
            </html>
            """

            try:
                connect.send(user.email, subject=subject, contents=content)
                connect.close()
                return True
            except (YagAddressError, YagInvalidEmailAddress):
                pass

        return False

    @classmethod
    def send_statement(self, user, period: Dict[str, str]):
        """ Sends the user's full statement to the registered email """
        if not user:
            return False

        dev_email, dev_password = _get_default_user()
        connect = yagmail.SMTP(dev_email, dev_password)

        df_html, summary = Statement.get_html_statement(user, period)
        df_html = df_html.replace('<table border="1"', '<table class="styled-table"')

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
                    background-color: #4CAF50;
                    color: #ffffff;
                    padding: 10px;
                    text-align: center;
                    border-radius: 10px 10px 0 0;
                }}
                .header h2 {{
                    margin: 0;
                    font-size: 24px;
                }}
                .content {{
                    padding: 20px;
                }}
                .content p {{
                    font-size: 16px;
                    line-height: 1.6;
                    margin: 10px 0;
                }}
                .statement-container {{
                    margin: 20px 0;
                }}
                .summary {{
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin: 20px 0;
                    padding: 10px;
                    border: 1px solid #ddd;
                    border-radius: 10px;
                    background-color: #f9f9f9;
                }}
                .money-in, .money-out {{
                    flex: 1;
                    text-align: center;
                    padding: 10px;
                    margin: 0 10px;
                    border-radius: 10px;
                    background-color: #e8f5e9;
                    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
                }}
                .money-in h4, .money-out h4 {{
                    margin: 5px 0;
                    font-size: 20px;
                    color: #2e7d32;
                }}
                .money-out h4 {{
                    color: #c62828;
                }}
                .money-in p, .money-out p {{
                    font-size: 16px;
                    margin: 0;
                    color: #555;
                }}
                .styled-table {{
                    width: 100%;
                    border-collapse: collapse;
                    font-size: 14px;
                    text-align: left;
                }}
                .styled-table th, .styled-table td {{
                    border: 1px solid #ddd;
                    padding: 8px;
                }}
                .styled-table th {{
                    background-color: #f4f4f4;
                }}
                .styled-table tr:nth-child(even) {{
                    background-color: #f9f9f9;
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
                    <h2>Expense Tracker</h2>
                </div>
                <div class="content">
                    <p>Dear {user.first_name},</p>
                    <p>We are pleased to inform you that your expense statement has been successfully generated. You can review your detailed expense report below:</p>
                    <div class="statement-container">
                        <h3>Name:</h3> <p>{user.first_name} {user.last_name} </p>
                        <h3>Email Address:</h3> <p> {user.email} </p>
                        <div class="summary">
                            <div class="money-in">
                                <p>Money In:</p>
                                <h4>{summary["Total_credit"]}</h4>
                            </div>
                            <div class="money-out">
                                <p>Money Out:</p>
                                <h4>{summary["Total_debit"]}</h4>
                            </div>
                        </div>
                    </div>
                    <div class="statement-container">
                        {df_html}
                    </div>
                    <p>If you have any questions or need assistance, feel free to reach out to us.</p>
                    <a href="http://127.0.0.1:5000/support" class="button">Contact Support</a>
                    <p class="italic">
                        If you did not request this statement, please reset your password or contact our support team for further assistance.
                    </p>
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
            connect.send(user.email, subject=subject, contents=content)
            connect.close()
            return True
        except (YagAddressError, YagInvalidEmailAddress):
            return False
