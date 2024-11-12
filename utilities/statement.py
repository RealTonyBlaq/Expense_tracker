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
            "Details": [user.first_name, user.last_name, user.email]
        })

        df.loc[len(df)] = ['', '']
        df.loc[len(df)] = ['', '']

        df2 = pd.DataFrame({
            'Date of Transaction': [d['Date_occurred'] for d in txns],
            'Description': [des['Description'] for des in txns],
            'Amount': [a['Amount'] for a in txns],
            'Transaction Type': [t['Type'] for t in txns]
        })

        empty_row_index = len(df) - 1

        # Split the DataFrame into two parts
        df_part1 = df.iloc[:empty_row_index + 1]  # Including the empty row
        df_part2 = df.iloc[empty_row_index + 1:]  # Remaining rows after the empty row

        df = pd.concat([df_part1, df2, df_part2])
        return [df, df2]
