#!/usr/bin/python3
""" The Category Model """

from models.base import BaseModel, Base
from sqlalchemy import Column, Integer, String, ForeignKey


class Income(BaseModel, Base):
    """ Defining the class category for the expenses """
    __tablename__ = "incomes"
    name = Column(String(60), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    amount = Column(Integer, nullable=False)
