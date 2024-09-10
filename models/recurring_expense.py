#!/usr/bin/env python3
""" The Recurring Expense Model """

from models.base import BaseModel, Base
from models.user import User
from sqlalchemy import Column, String, DECIMAL, ForeignKey, DATE, Enum
from sqlalchemy.dialects.sqlite import TEXT
from sqlalchemy.orm import relationship


class RecurringExpense(BaseModel, Base):
    """ Defines a model for recurring expenses """
    __tablename__ = 'recurring_expenses'

    category_id = Column(String(60),
                         ForeignKey('categories.id', ondelete='SET NULL'),
                         nullable=False)
    user_id = Column(String(60),
                     ForeignKey('users.id', ondelete='CASCADE'),
                     nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    start_date = Column(DATE, nullable=False)
    end_date = Column(DATE)
    frequency = Column(Enum('Daily'))
    description = Column(TEXT)
