#!/usr/bin/env python3
""" The association tables """

from models.base import Base
from sqlalchemy import Column, String, ForeignKey


class ExpenseTag(Base):
    """ Association table for the Expense Table and Tag table """
    __tablename__ = 'expense_tag'

    expense_id = Column(String(60),
                        ForeignKey('expenses.id', ondelete='CASCADE'),
                        primary_key=True)
    tag_id = Column(String(60),
                    ForeignKey('tags.id', ondelete='CASCADE'),
                    primary_key=True)
