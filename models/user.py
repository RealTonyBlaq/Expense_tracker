#!/usr/bin/python3
""" The User Model """

from models.base import Base, BaseModel
from models.category import Category
from models.expense import Expense
from sqlalchemy import String, Column
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """ Defining the User class """
    __tablename__ = "users"
    first_name = Column(String(60), nullable=False)
    last_name = Column(String(60), nullable=False)
    email = Column(String(60), nullable=False)
    password = Column(String(60), nullable=False)
    categories = relationship("Category", backref="users",
                              cascade="all, delete, delete-orphan")

    def details(self):
        """
        Returns a dictionary containing information about a user
        including a list of dictionaries with <category.name>.<category.id>
        as key and a list of expenses as the value pair
        """
        from models import storage
        categories = storage.all(Category)
        user_dict = {}
        for key, value in self.__dict__.items():
            if key != "password":
                user_dict[key] = value

        for category in categories.values():
            if category.user_id == self.id:
                key = "{}.{}".format(category.name, category.id)
                new = {key: []}
                for 
