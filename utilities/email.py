#!/usr/bin/env python3
""" Email service for Expense Tracker """

import yagmail
from yagmail.error import YagInvalidEmailAddress, YagAddressError


class Email:
    """ Defining the Email class """
    from api.v1.app import app

    dev_email = app.config['MAIL_DEFAULT_SENDER']
    dev_password = app.config['MAIL_PASSWORD']


    @classmethod
    def send(self, email: str, subject: str, content: str) -> bool:
        """ sends a confirmation email with token """
        

        if email and subject and content:
            connect = yagmail.SMTP(dev_email, dev_password)

            try:
                connect.send(email, subject=subject, contents=content)
                connect.close()
                return True
            except (YagAddressError, YagInvalidEmailAddress):
                pass

        return False

    def send_statement(self, )
