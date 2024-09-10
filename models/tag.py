#!/usr/bin/env python3
""" The Tag Model """

from models.associations import ExpenseTag
from models.base import BaseModel, Base
from models.expense import Expense
from models.user import User
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class Tag(BaseModel, Base):
    """ Tags provides additional categorization/labelling for an expense """
    __tablename__ = 'tags'

    name = Column(String(60), nullable=False, unique=True)
    user_id = Column(String(60),
                     ForeignKey('users.id', ondelete='CASCADE'),
                     nullable=False)

    user = relationship('User', back_populates='tags')
    expenses = relationship('ExpenseTag', secondary='expense_tag', back_populates='tags')
