#!/usr/bin/python3
""" Module for API route for the User """

from api import ETapp
from flask import abort, jsonify, make_response
from models import storage
from models.user import User


ETapp.route('/users', strict_slashes=False)
ETapp.route('/users/<id>', strict_slashes=False)
def retrieve(id=None):
    """
    Returns a dict/list with all user objects or a single user if id is not None
    """
    if id:
        obj = storage.find(User, id)
        if obj:
            return jsonify(obj.details())
        abort(404)
    else:
        users = []
        for obj in storage.all(User).values():
            users.append(obj.details())

        return jsonify(users)


@ETapp.route('/users/<id>', methods=['DELETE'],
             strict_slashes=False)
def delete(id):
    """ Deletes a User object if id exists """
    user = storage.find()
