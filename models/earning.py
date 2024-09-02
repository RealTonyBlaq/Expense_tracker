#!/usr/bin/python3
""" The Category Model """

from models.base import BaseModel, Base
from sqlalchemy import Column, Integer, String, ForeignKey, Date


class Earning(BaseModel, Base):
    """ Defining the Earnings class """
    __tablename__ = "earnings"
    name = Column(String(60), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    date_occurred = Column(Date, nullable=False)
    amount = Column(Integer, nullable=False)
    description = Column(String(128), nullable=True)
