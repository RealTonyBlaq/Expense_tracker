#!/usr/bin/python3
""" The Expense Model """

from models.base import Base, BaseModel
from sqlalchemy import Column, String, ForeignKey, Date, DECIMAL
from sqlalchemy.dialects.sqlite import TEXT
from sqlalchemy.orm import relationship


class Expense(BaseModel, Base):
    """ The Expense Class holds the expenses made by the User """
    __tablename__ = 'expenses'
    category_id = Column(String(60),
                         ForeignKey('categories.id',), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id', ondelete='CASCADE'),
                         nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    date_occurred = Column(Date, nullable=False)
    description = Column(TEXT, nullable=True)

    # Relationships
    user = relationship('User', back_populates='expenses')
    category = relationship('Category', back_populates='expenses')
    tags = relationship('ExpenseTag', secondary='expense_tag',
                        back_populates='expenses')
