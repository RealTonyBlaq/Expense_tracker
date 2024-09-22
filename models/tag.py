#!/usr/bin/env python3
""" The Tag Model """

from models.associations import expense_tag
from models.base import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class Tag(BaseModel, Base):
    """ Tags provides additional categorization/labelling for an expense """
    __tablename__ = 'tags'

    name = Column(String(60), nullable=False, unique=True)
    user_id = Column(String(60),
                     ForeignKey('users.id', ondelete='CASCADE'),
                     nullable=False)

    # Relationships
    user = relationship('User', back_populates='tags')
    expenses = relationship('Expense', secondary=expense_tag, back_populates='tags')
