#!/usr/bin/python3
""" The User Model """

from models.base import Base, BaseModel
from models.income import Income
from models.expense import Expense
from sqlalchemy import String, Column
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """ Defining the User class """
    __tablename__ = "users"
    first_name = Column(String(60), nullable=False)
    last_name = Column(String(60), nullable=False)
    email = Column(String(60), nullable=False, unique=True)
    password = Column(String(60), nullable=False)
    incomes = relationship("Income", backref="users",
                              cascade="all, delete, delete-orphan")
    expenses = relationship('Expense', backref='users',
                            cascade="all, delete, delete-orphan")

    def details(self):
        """
        Returns a dictionary containing information about a user
        including a list of dictionaries with <category.name>.<category.id>
        as key and a list of expenses as the value pair
        """
        from models import storage
        incomes = storage.all(Income)
        expenses = storage.all(Expense)
        user_dict = {}
        for key, value in self.__dict__.items():
            if key not in ["password", 'categories', '_sa_instance_state']:
                user_dict[key] = value
        user_dict['incomes'] = []
        user_dict['expenses'] = []
        for income in incomes.values():
            if income.user_id == self.id:
                user_dict["incomes"].append(income.about())

        for expense in expenses.values():
            if expense.user_id == self.id:
                user_dict["expenses"].append(expense.about())

        return user_dict
