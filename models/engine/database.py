#!/usr/bin/python3
""" Storage Model """

from models.base import Base
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


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

    def reload()
