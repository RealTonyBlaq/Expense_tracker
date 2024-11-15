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

    def __init__(self, **kwargs: dict) -> None:
        """ """
        self.id = str(uuid4())
        self.created_at = datetime.now()
        self.updated_at = self.created_at
        if kwargs:
            for key, value in kwargs.items():
                if key not in ['id', 'created_at', 'updated_at']:
                    setattr(self, key, value)

    def __str__(self) -> str:
        """ Returns a string representation of the Object """
        return "[{}].{} ({})".format(self.__class__.__name__, self.id,
                                     self.to_dict())

    def to_dict(self) -> dict:
        """ Returns a dictionary of the object's key-value pairs """
        from utilities import db
        obj = db.query(self.__class__).filter_by(id=self.id).first()
        if not obj:
            return {}

        obj_dict = {}
        obj_dict['type'] = self.__class__.__name__
        for key, value in obj.__dict__.items():
            if key not in ['_sa_instance_state', 'password', 'token']:
                obj_dict[key] = value
        return obj_dict

    def save(self) -> None:
        """ Save an object to storage """
        from utilities import db
        self.updated_at = datetime.now()
        db.add(self)
        db.save()

    def delete(self) -> None:
        """ Deletes the object from the database """
        from utilities import db
        db.delete(self)
