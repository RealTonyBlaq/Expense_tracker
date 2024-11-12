#!/usr/bin/env python3
""" The Transaction Statement Excel generator """

import pandas as pd
from openpyxl import load_workbook
from models.user import User


class Statement:
    """ The statement class """

    @classmethod
    def get_excel_file(self, user: User):
        """ Returns the Excel workbook """
        txns = user.generate_statement()

        df = pd.DataFrame({
            "Contact Information": ['First Name', 'Last Name', 'Email'],
            "Details": [user.first_name, user.last_name]
        })
