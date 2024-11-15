#!/usr/bin/env python3
""" Email service for Expense Tracker """

from utilities.statement import Statement
import yagmail
from yagmail.error import YagInvalidEmailAddress, YagAddressError


def _get_default_user() -> list:
    """ Helper function to return Default Mail details """
    from api.v1.app import app

    return [app.config['MAIL_DEFAULT_SENDER'], app.config['MAIL_PASSWORD']]


class Email:
    """ Defining the Email class """

    @classmethod
    def send(self, email: str, subject: str, content: str) -> bool:
        """ sends a confirmation email with token """
        if email and subject and content:
            dev_email, dev_password = _get_default_user()
            connect = yagmail.SMTP(dev_email, dev_password)
            try:
                connect.send(email, subject=subject, contents=content)
                connect.close()
                return True
            except (YagAddressError, YagInvalidEmailAddress):
                pass

        return False

    @classmethod
    def send_statement(self, user):
        """ Sends the user's full statement to the user """
        if not user:
            return False

        dev_email, dev_password = _get_default_user()
        connect = yagmail.SMTP(dev_email, dev_password)

        df_html = Statement.get_html(user)
        subject = "Expense statement - Expense Tracker"
        content = f"""
        Dear {user.first_name} {user.last_name},

        Your statement was generated successfully!
        Kindly find your statement below:
        {df_html}

        Regards,

        Expense Tracker Team.

        If you did not initiate this kindly reset your password \
            or contact the team for further assistance.
        """

        try:
            connect.send(user.email, subject=subject, contents=content)
            connect.close()
            return True
        except (YagAddressError, YagInvalidEmailAddress):
            return False
