#!/usr/bin/env python3
""" The Category Model """

from models.base import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class Category(BaseModel, Base):
    """ Category Model that groups Expense objects """
    __tablename__ = 'categories'
    name = Column(String(60), nullable=False)
    user_id = Column(String(60),
                     ForeignKey('users.id', ondelete='CASCADE'),
                     nullable=False)

    # Relationships
    user = relationship('User', back_populates='categories')
    expenses = relationship('Expense', backref='users',
                            cascade='all, delete, delete-orphan')
    recurring_expenses = relationship('RecurringExpense', backref='users',
                                      cascade='all, delete, delete-orphan')
