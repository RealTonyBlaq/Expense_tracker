#!/usr/bin/python3
""" Storage Model """

from datetime import datetime
from models.base import Base
from models.category import Category
from models.expense import Expense
from auth.user_session import UserSession
from models.user import User
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.exc import NoResultFound, InvalidRequestError
from sqlalchemy.orm import scoped_session, sessionmaker


classes = [User, Category, Expense]


class Database:
    """ Defining the Database storage Model """
    __engine = None
    __session = None

    def __init__(self) -> None:
        """ Initializing attributes """
        USER = getenv('ET_DB_USER')
        PASSWORD = getenv('ET_DB_PWD')
        HOST = getenv('ET_DB_HOST')
        DB = getenv('ET_DB')
        self.__engine = create_engine('mysql://{}:{}@{}:3306/{}'
                                      .format(USER, PASSWORD, HOST, DB))
        if getenv('BUILD_TYPE') == 'test':
            Base.metadata.drop_all(self.__engine)

    def reload(self) -> None:
        """ Reloads data from the database """
        Base.metadata.create_all(self.__engine)
        sess = sessionmaker(bind=self.__engine, expire_on_commit=False)
        session = scoped_session(sess)
        self.__session = session

    def all(self, cls=None) -> dict:
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

    def add(self, obj) -> None:
        """ Adds a new object to the current session  """
        if obj:
            self.__session.add(obj)

    def save(self) -> None:
        """ Commits all added objects to storage """
        self.__session.commit()

    def close(self) -> None:
        """ Calls the remove() on the database session """
        self.__session.remove()

    def find(self, cls, id: str):
        """ Retrieves an obj from storage based on its id and class """
        if cls and id:
            for obj in self.all(cls).values():
                if obj.id == id:
                    return obj
            raise ValueError(f'{cls.__name__} with id does not exist')
        raise TypeError(f'{cls.__name__} and/or id cannot be None')

    def delete(self, obj) -> None:
        """ Deletes an object and calls save """
        if obj:
            self.__session.delete(obj)
            self.save()

    def get_user(self, email) -> User:
        """ Retrieves a User obj from storage if the email matches """
        if email:
            users = self.all(User).values()
            for user in users:
                if user.email == email:
                    return user
        raise ValueError(f'User -> {email} not found')

    def update_password(self, user_id: str, hashed_password: str) -> None:
        """ Updates a User's password """
        if user_id and hashed_password:
            try:
                user = self.find(User, user_id)
            except (ValueError, TypeError):
                return None

            setattr(user, 'password', hashed_password)
            user.save()
        return None

    def fetch_session_obj_by(self, **kwargs) -> UserSession:
        """ Returns a UserSession obj if it exists """
        if kwargs:
            try:
                sess_obj = self.__session.query(UserSession).filter_by(**kwargs).first()
                return sess_obj
            except (InvalidRequestError, NoResultFound):
                pass
        return None
