#!/usr/bin/python3
""" The Expense Model """

from models.base import Base, BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey


class Expense(BaseModel, Base):
    """ Defining the Expense Class """
    __tablename__ = 'expenses'
    name = Column(String(60), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'),
                         nullable=False)
    amount = Column(Integer, nullable=False)
    description = Column(String(128), nullable=True)
