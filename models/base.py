#!/usr/bin/python3
""" The Base Model for other classes/models """

from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from uuid import uuid4


Base = declarative_base()


class BaseModel:
    """ Defines the BaseModel class """
    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at
