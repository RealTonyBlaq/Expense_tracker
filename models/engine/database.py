#!/usr/bin/python3
""" Storage Model """

from datetime import datetime
from models.base import Base
from models.category import Category
from models.expense import Expense
from models.user import User
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


classes = [Category, Expense, User]


class Database:
    """ Defining the Database storage Model """
    __engine = None
    __session = None

    def __init__(self):
        """ Initializing attributes """
        USER = getenv('ET_DB_USER')
        PASSWORD = getenv('ET_DB_PWD')
        HOST = getenv('ET_DB_HOST')
        DB = getenv('ET_DB')
        self.__engine = create_engine('mysqldb://{}:{}@{}/{}'.format(USER,
                                                                     PASSWORD,
                                                                     HOST,
                                                                     DB))

    def reload(self):
        """ Reloads data from the database """
        Base.metadata.create_all(self.__engine)
        sess = sessionmaker(bind=self.__engine, expire_on_commit=False)
        session = scoped_session(sess)
        self.__session = session

    def all(self, cls=None):
        """ Retrieves all objs of a class from storage """
        objs = {}
        if cls:
            ins = self.__session.query(cls)
            for row in ins:
                objs['{}.{}'.format(cls.__name__, row.id)] = row
        else:
            for clas in classes:
                ins = self.__session.query(clas)
                for row in ins:
                    objs['{}.{}'.format(clas.__name__, row.id)] = row
        return objs

    def add(self, obj):
        """ Adds a new object to the current session  """
        if obj:
            self.__session.add(obj)

    def save(self, obj):
        """ Saves an object to db, updates the updated_at elem """
        if obj:
            obj.updated
