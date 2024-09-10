#!/usr/bin/env python3
""" The Category Model """

from models.base import BaseModel, Base
from models.user import User
from models.expense import Expense
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class Category(BaseModel, Base):
    """ Category Model that groups Expense objects """
    __tablename__ = 'categories'

    name = Column(String(60), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    expenses = relationship('Expense', backref='users',
                            cascade='all, delete, delete-orphan')
