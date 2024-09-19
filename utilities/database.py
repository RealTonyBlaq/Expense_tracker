#!/usr/bin/python3
""" Storage Model """

from datetime import datetime
from models.base import Base
from models.category import Category
from models.earning import Earning
from models.expense import Expense
from models.recurring_expense import RecurringExpense
from models.tag import Tag
from models.user import User
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.exc import NoResultFound, InvalidRequestError
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm.session import Session


classes = [User, Category, Earning, Expense, Tag, RecurringExpense]


class Database:
    """ Defining the Database storage Model """
    __engine = None

    def __init__(self) -> None:
        """ Initializing attributes """
        USER = getenv('ET_DB_USER')
        PASSWORD = getenv('ET_DB_PWD')
        HOST = getenv('ET_DB_HOST')
        DB = getenv('ET_DB')
        # self.__engine = create_engine('mysql://{}:{}@{}:3306/{}'
        #                              .format(USER, PASSWORD, HOST, DB))
        self.__engine = create_engine("sqlite:///et.db", echo=False)
        Base.metadata.create_all(self.__engine)
        self.__session = None
        if getenv('BUILD_TYPE') == 'test':
            Base.metadata.drop_all(self.__engine)

    def reload(self) -> Session:
        """ Returns the query object """
        return self._session

    def query(self, cls):
        """ Returns the query object """
        return self._session.query(cls)

    @property
    def _session(self) -> Session:
        """ Reloads data from the database """
        if self.__session is None:
            session = sessionmaker(bind=self.__engine, expire_on_commit=False)
            self.__session = scoped_session(session)
        return self.__session

    def all(self, cls=None) -> dict:
        """ Retrieves all objs of a class from storage """
        objs = {}
        if cls:
            ins = self._session.query(cls)
            for row in ins:
                objs['{}.{}'.format(cls.__name__, row.id)] = row
        else:
            for clas in classes:
                ins = self._session.query(clas)
                for row in ins:
                    objs['{}.{}'.format(clas.__name__, row.id)] = row
        return objs

    def add(self, obj) -> None:
        """ Adds a new object to the current session  """
        if obj:
            self._session.add(obj)

    def save(self) -> None:
        """ Commits all added objects to storage """
        self._session.commit()

    def close(self) -> None:
        """ Calls the remove() on the database session """
        self._session.close()

    def find(self, cls, id: str):
        """ Retrieves an obj from storage based on its id and class """
        if cls and id:
            for obj in self.all(cls).values():
                if obj.id == id:
                    return obj
            raise ValueError(f'{cls.__name__} with {id} does not exist')
        raise TypeError('cls and/or id cannot be None')

    def delete(self, obj) -> None:
        """ Deletes an object and calls save """
        if obj:
            self._session.delete(obj)
            self.save()

    def get_user(self, email) -> User:
        """ Retrieves a User obj from storage if the email matches """
        if email:
            users = self.all(User).values()
            for user in users:
                if user.email == email:
                    return user
        raise ValueError(f'User with {email} not found')
