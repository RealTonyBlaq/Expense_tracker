#!/usr/bin/env python3
""" Email service for Expense Tracker """

from utilities.statement import Statement
import yagmail
from yagmail.error import YagInvalidEmailAddress, YagAddressError


class Email:
    """ Defining the Email class """

    def __init__(self):
        """ Inintializes the variables """
        from api.v1.app import app
        dev_email = app.config['MAIL_DEFAULT_SENDER']
        dev_password = app.config['MAIL_PASSWORD']
        self.connect = yagmail.SMTP(dev_email, dev_password)

    @classmethod
    def send(self, email: str, subject: str, content: str) -> bool:
        """ sends a confirmation email with token """
        if email and subject and content:
            try:
                self.connect.send(email, subject=subject, contents=content)
                self.connect.close()
                return True
            except (YagAddressError, YagInvalidEmailAddress):
                pass

        return False

    def send_statement(self, user):
        """ Sends the user's full statement to the user """
        df_html = Statement.get_html(user)
        
