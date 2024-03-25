#!/usr/bin/python3
""" Module for API route for the User """

from api import ETapp
from models import storage
from models.user import User


ETapp.route('/users', strict_slashes=False)
ETapp.route('/users/<id>', strict_slashes=False)
def retrieve(id=None):
    """
    Returns a dict with all user objects or a single user if id is not None
    """
    if
