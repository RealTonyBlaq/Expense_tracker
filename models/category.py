#!/usr/bin/python3
""" The Category Model """

from models.base import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class Category(BaseModel, Base):
    """ Defining the class category for the expenses """
    __tablename__ = "categories"
    name = Column(String(60), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    expenses = relationship('Expense', backref='categories',
                            cascade='all, delete, delete-orphan')
