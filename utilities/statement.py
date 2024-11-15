#!/usr/bin/env python3
""" The Transaction Statement Excel generator """

import pandas as pd
from openpyxl import load_workbook
from models.user import User


class Statement:
    """ The statement class """

    @classmethod
    def get_html(self, user: User):
        """ Returns the Excel workbook """
        txns = user.generate_statement()
        df = pd.DataFrame({
            'Date of Transaction': [d['Date_occurred'] for d in txns],
            'Description': [des['Description'] for des in txns],
            'Amount': [a['Amount'] for a in txns],
            'Transaction Type': ['Credit' if t.get('Type') == 'Earning' else 'Debit' for t in txns]
        })

        return df.to_html(index=False)
