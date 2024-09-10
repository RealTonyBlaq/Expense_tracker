#!/usr/bin/env python3
""" The Category Model """

from models.base import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class Category(BaseModel, Base):
    """ Category Model that groups Expense objects """
    __tablename__ = 'categories'

    name = Column(String(60), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'))
