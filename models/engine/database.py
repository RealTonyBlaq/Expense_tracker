#!/usr/bin/python3
""" Storage Model """

from models.base import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


class Database:
    """ Defining the Database storage Model """
    __engine = None
    __session = None

    def __init__(self):
        """ Initializing attributes """
        USER = getenv('')
        self.__engine = create_engine('mysqldb://{}:{}@{}/{}'.format())
