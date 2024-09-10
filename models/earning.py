#!/usr/bin/python3
""" The Category Model """

from models.base import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Date, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.sqlite import TEXT


class Earning(BaseModel, Base):
    """ Defining the Earnings class """
    __tablename__ = "earnings"
    name = Column(String(60), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    date_occurred = Column(Date, nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    description = Column(TEXT, nullable=True)

    # Relationships
    user = relationship('User', back_populates='earnings')
