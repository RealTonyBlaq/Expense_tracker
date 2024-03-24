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

    def increase_by(self, value):
        """ Increases the amount of an Expense """
        if isinstance(value, int):
            self.amount += value
        else:
            raise TypeError('Value must be an Integer')

    def decrease_by(self, value):
        """ Decreases the amount of an expense by a value """
        if isinstance(value, int):
            if value <= self.amount:
                self.amount -= value
            else:
                raise ValueError('Value must be <= {}'.format(self.amount))
        else:
            raise TypeError('Value must be an Integer')
