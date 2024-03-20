#!/usr/bin/python3
""" The Category Model """

from models.base import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey


class Category(BaseModel, Base):
    """ Defining the class category for the expenses """
    name = Column(String(60), )
