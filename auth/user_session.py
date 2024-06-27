#!/usr/bin/env python3
""" User Session class """

from models.base import BaseModel, Base
from sqlalchemy import Column, Integer, String, ForeignKey


class UserSession(BaseModel, Base):
    """ Defining the user session class """
    __tablename__ = 'user_sessions'
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    reset_token = Column(Integer)

    def __init__(self, **kwargs: dict) -> None:
        """ Initializes the attributes """
        super().__init__(**kwargs)
