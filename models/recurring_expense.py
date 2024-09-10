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

    
