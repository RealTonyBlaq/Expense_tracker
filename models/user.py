#!/usr/bin/python3
""" The User Model """

from models.base import Base, BaseModel
from sqlalchemy import String, Integer, Column


class User(BaseModel, Base):
    """ Defining the User class """
    first_name = Column(String(60), nullable=False)
    last_name = Column(String(60), nullable=False)
    email = Column(String)
