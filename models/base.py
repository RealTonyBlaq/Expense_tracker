#!/usr/bin/python3
""" The Base Model for other classes/models """

from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, String
from uuid import uuid4


Base = declarative_base()


class BaseModel:
    """ Defines the BaseModel class """
    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    def __init__(self, **kwargs):
        """ """
        self.id = str(uuid4())
        self.created_at = datetime.now()
        self.updated_at = self.created_at
        if kwargs:
            for key, value in kwargs.items():
                if key not in ['id', 'created_at', 'updated_at']:
                    setattr(self, key, value)
        if '_sa_instance_state' in self.__dict__:
            del self.__dict__['_sa_instance_state']

    def __str__(self):
        """ Returns a string representation of the Object """
        return "[{}].{} ({})".format(self.__class__.__name__, self.id,
                                     self.about())

    def about(self):
        """ Returns a dictionary of the object's key-value pairs """
        obj_dict = {}
        for key, value in self.__dict__.items():
            obj_dict[key] = value
        return obj_dict

    def save(self):
        """ Save an object to storage """
        from models import storage
        self.updated_at = datetime.now()
        storage.add(self)
        storage.save()
