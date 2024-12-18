#!/usr/bin/env python3
""" The Recurring Expense Model """

from models.base import BaseModel, Base
from sqlalchemy import Column, String, DECIMAL, ForeignKey, DateTime, Enum
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
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime)
    frequency = Column(Enum('daily', 'weekly', 'monthly',
                            name='frequency_enum'), nullable=False)
    description = Column(TEXT)

    # Relationships
    user = relationship('User', back_populates='recurring_expenses')
    category = relationship('Category', back_populates='recurring_expenses',
                            overlaps='users')
