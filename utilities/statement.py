#!/usr/bin/env python3
""" The Transaction Statement Excel generator """

import pandas as pd
from models.user import User
from typing import Dict


class Statement:
    """ The statement class """

    @classmethod
    def get_html_statement(self, user: User, period:Dict[str, str] = None):
        """ Returns the Excel workbook """
        txns = user.generate_statement(period)
        money_in, money_out = 0.0, 0.0

        for t in txns:
            if t['Type'] == 'Earning':
                money_in += t['Amount']
            else:
                money_out += t['Amount']

        summary = {'Total_credit': money_in,
                   'Total_debit': money_out,
                   'Balance': money_in - money_out
        }

        df = pd.DataFrame({
            'Date of Transaction': [d['Date_occurred'] for d in txns],
            'Description': [des['Description'] for des in txns],
            'Transaction Type': ['Credit' if t.get('Type') == 'Earning' else 'Debit' for t in txns],
            'Amount': [a['Amount'] for a in txns]
        })

        return df.to_html(index=False, classes='styled-table', border=0), summary
