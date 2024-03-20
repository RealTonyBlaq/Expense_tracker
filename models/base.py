#!/usr/bin/python3
""" The Base Model for other classes/models """

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String


Base = declarative_base()

class BaseModel:
    """ Defines the BaseModel class """
    