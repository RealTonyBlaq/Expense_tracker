#!/usr/bin/python3
""" The Expense Model """

from models.base import Base, BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey


class Expense(BaseModel, Base):
    """ Defining the Expense Class """
    __tablename__ = 'expenses'
    category_id = Column(String(60), ForeignKey('categories.id'),
                         nullable=False)
    amount = Column(Integer, nullable=False)
    description = Column(String(128), nullable=True)

    def to_dict(self):
        """
        Returns a dictionary containing key-value pairs of
        the attributes an expense object
        """
        for key, value in 
