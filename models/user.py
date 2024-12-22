#!/usr/bin/python3
""" The User Model """

from datetime import datetime
from flask_login import UserMixin
from models.base import Base, BaseModel
from os import getenv
from sqlalchemy import String, Column, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.sqlite import TEXT
from typing import Dict, Tuple, List


format = "%d %b, %Y %H:%M:%S"
currency = getenv('DEFAULT_CURRENCY', '$')


def get_bal_before_period(sorted_txns: List[Dict],
                          period: Dict[str, str]) -> float:
    """ Gets the balance brought forward """
    start_date = period['from']
    for txn in sorted_txns:
        if txn['Date_occurred'] < start_date:
            return txn['Balance']

    return 0.00


class User(UserMixin, BaseModel, Base):
    """ Defining the User class """
    __tablename__ = "users"
    first_name = Column(String(60), nullable=False)
    last_name = Column(String(60), nullable=False)
    email = Column(String(60), nullable=False, unique=True)
    phone = Column(String(15), unique=True, nullable=True)
    password = Column(String(60), nullable=False)
    last_login_time = Column(DateTime, default=None)
    is_email_verified = Column(Boolean, default=False)
    is_2fa_enabled = Column(Boolean, default=False)
    bio = Column(TEXT, nullable=True)
    is_logged_in = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)

    # Relationships
    earnings = relationship("Earning", back_populates="user",
                              cascade="all, delete, delete-orphan")
    expenses = relationship('Expense', back_populates='user',
                            cascade="all, delete, delete-orphan")
    categories = relationship('Category', back_populates='user',
                              cascade='all, delete, delete-orphan')
    tags = relationship('Tag', back_populates='user',
                        cascade='all, delete, delete-orphan')
    recurring_expenses = relationship('RecurringExpense', back_populates='user',
                                      cascade='all, delete, delete-orphan')

    @property
    def is_active(self) -> bool:
        """ Returns whether a user is authenticated/verified """
        return self.is_email_verified

    @property
    def is_authenticated(self) -> bool:
        """ Returns whether a user is logged in """
        return self.is_logged_in

    def generate_statement(self, period: Dict[str, str] = None) -> Tuple[list, dict]:
        """ Return:
                Sorted list dictionaries of Earning, Expense and RecurringExpense objects
                    with the necessary transaction details
                A summary dict containing total credits, total debits and the balance
        """
        earnings = [e.to_dict() for e in self.earnings]
        expenses = [ex.to_dict() for ex in self.expenses]
        recurring_expenses = [r.to_dict() for r in self.recurring_expenses]

        all_txns = earnings + expenses + recurring_expenses
        sorted_txns = sorted(all_txns,
                             key=lambda x: x.get('date_occurred') or x.get('start_date'))

        txns = []
        helper_list = []
        balance = 0.00
        money_in = 0.00
        money_out = 0.00
        start_date = period['from']
        end_date = period['to']

        for t in sorted_txns:
            record = {'Type': 'Credit' if t.get('type') == 'Earning' else 'Debit',
                      'Amount': float(t.get('amount')),
                      'Date_occurred': t.get('date_occurred') or t.get('start_date'),
                      'Description': t.get('description'),
                      'Balance': 0.00}

            if record['Type'] == 'Credit':
                balance += record['Amount']
            else:
                balance -= record['Amount']

            record['Balance'] = balance
            helper_list.append(record.copy())
            if start_date <= record['Date_occurred'] <= end_date:
                if record['Type'] == 'Credit':
                    money_in += record['Amount']
                else:
                    money_out += record['Amount']
                record['Date_occurred'] = datetime.strftime(record['Date_occurred'], format)
                txns.append(record)

        # reverse the lists
        helper_list.reverse()
        txns.reverse()

        opening_balance = f'{currency} {get_bal_before_period(helper_list, period):,.2f}'
        summary = {'Total_credit': f'{currency} {money_in:,.2f}',
                   'Total_debit': f'{currency} {money_out:,.2f}',
                   'Opening_balance': opening_balance,
                   'Closing_balance': f'{currency} {txns[0]["Balance"]:,.2f}' if txns != [] else f'{currency} {0.00}',
                   'Balance': f'{currency} {money_in - money_out:,.2f}'
        }

        return txns, summary
