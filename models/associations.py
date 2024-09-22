#!/usr/bin/env python3
""" The association tables """

from models.base import Base
from sqlalchemy import Column, String, ForeignKey, Table


expense_tag = Table(
    "ExpenseTag",
    Base.metadata,
    Column('expense_id', String(60),
           ForeignKey('expenses.id', ondelete='CASCADE'), primary_key=True),
    Column('tag_id', String(60),
           ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True)
)
