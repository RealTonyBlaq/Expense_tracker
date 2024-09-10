#!/usr/bin/env python3
""" The Category Model """

from models.base import BaseModel, Base
from sqlalchemy import Column, String


class Category(BaseModel, Base):
    """ Category Model that groups Expense objects """
    