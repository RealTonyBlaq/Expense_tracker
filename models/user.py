#!/usr/bin/python3
""" The User Model """

from models.base import Base, BaseModel
from sqlalchemy import String, Integer


class User(BaseModel, Base):
    """ Defining the User class """
