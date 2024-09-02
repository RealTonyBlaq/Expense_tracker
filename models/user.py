#!/usr/bin/python3
""" The User Model """

from flask_login import UserMixin
from models.base import Base, BaseModel
from models.earning import Earning
from models.expense import Expense
from sqlalchemy import String, Column, Boolean, DateTime, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.sqlite import TEXT


class User(UserMixin, BaseModel, Base):
    """ Defining the User class """
    __tablename__ = "users"
    first_name = Column(String(60), nullable=False)
    last_name = Column(String(60), nullable=False)
    email = Column(String(60), nullable=False, unique=True)
    password = Column(String(60), nullable=False)
    token = Column(Integer, default=0)
    last_login_time = Column(DateTime, default=None)
    is_email_verified = Column(Boolean, default=False)
    bio = Column(TEXT, nullable=True)
    is_logged_in = Column(Boolean, default=False)
    earnings = relationship("Earning", backref="users",
                              cascade="all, delete, delete-orphan")
    expenses = relationship('Expense', backref='users',
                            cascade="all, delete, delete-orphan")

    @property
    def is_active(self):
        """ Returns whether a user is authenticated/verified """
        return self.is_email_verified

    @property
    def is_authenticated(self):
        """ Returns whether a user is logged in """
        return self.is_logged_in
