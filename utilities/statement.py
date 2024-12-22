#!/usr/bin/env python3
""" The Transaction Statement Excel generator """

import pandas as pd
from models.user import User
from os import getenv
from typing import Dict


currency = getenv('DEFAULT_CURRENCY', '$')


class Statement:
    """ The statement class """

    @classmethod
    def get_html_statement(self, user: User, period:Dict[str, str] = None):
        """ Returns the HTML Excel workbook """
        txns, summary = user.generate_statement(period)

        df = pd.DataFrame({
            'Date of Transaction': [d['Date_occurred'] for d in txns],
            'Description': [des['Description'] for des in txns],
            'Transaction Type': [t['Type'] for t in txns],
            'Amount': [a['Amount'] for a in txns],
            'Balance': [b['Balance'] for b in txns]
        })

        def format_with_color(value):
            """ Format value with red color if negative """
            formatted = f"{value:,.2f}"
            if value < 0:
                return f'<span style="color:red;">{currency} {formatted}</span>'
            return f"{currency} {formatted}"


        df['Amount'] = df['Amount'].apply(format_with_color)
        df['Balance'] = df['Balance'].apply(format_with_color)

        html = df.to_html(index=False, classes='styled-table', border=0, escape=False)

        return html, summary
