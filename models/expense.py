#!/usr/bin/python3
""" The Expense Model """

from models.base import Base, BaseModel
from models.u
from sqlalchemy import Column, String, ForeignKey, Date, DECIMAL
from sqlalchemy.dialects.sqlite import TEXT
from sqlalchemy.orm import relationship


class Expense(BaseModel, Base):
    """ The Expense Class holds the expenses made by the User """
    __tablename__ = 'expenses'

    category_id = Column(String(60), ForeignKey('categories.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'),
                         nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    date_occurred = Column(Date, nullable=False)
    description = Column(TEXT, nullable=True)

    user = relationship('User')
