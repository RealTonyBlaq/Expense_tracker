#!/usr/bin/python3
""" API route for the User """

from api import ETapp
from flask import abort, jsonify, make_response, request
from models import storage
from models.user import User


@ETapp.route('/users', strict_slashes=False)
@ETapp.route('/users/<id>', strict_slashes=False)
def retrieve(id=None):
    """
    Returns a dict/list with all user objects or a single user
    if id is not None
    """
    if id:
        obj = storage.find(User, id)
        if obj:
            return make_response(jsonify(obj.details()), 200)
        abort(404)
    else:
        users = []
        for obj in storage.all(User).values():
            users.append(obj.details())

        return make_response(jsonify(users), 200)


@ETapp.route('/users/<id>', methods=['DELETE'],
             strict_slashes=False)
def delete(id):
    """ Deletes a User object if id exists """
    user = storage.find(User, id)
    if user:
        storage.delete(user)
        return make_response(jsonify({}), 200)
    abort(404)


@ETapp.route('/users', methods=['POST'],
             strict_slashes=False)
def create():
    """ Creates a new User object """
    if request.is_json is True:
        data = request.get_json()
        if 'first_name' not in data:
            abort(400, 'first_name missing')
        if 'last_name' not in data:
            abort(400, 'last_name missing')
        if 'email' not in data:
            abort(400, 'email missing')
        if 'password' not in data:
            abort(400, 'password missing')
        user = User(**data)
        user.save()
        return make_response(jsonify(user.details()), 201)
    abort(400, 'Not a JSON')


@ETapp.route('/users/<id>', methods=['PUT'],
             strict_slashes=False)
def update(id):
    """ Updates a user based on request data """
    if request.is_json is True:
        data = request.get_json()
        obj = storage.find(User, id)
        if obj:
            for key, value in data.items():
                if key not in ['password', 'id', 'created_at', 'updated_at']:
                    setattr(obj, key, value)
            obj.save()
            return make_response(jsonify(obj.details()), 200)
        abort(404)
    abort(400, 'Not a JSON')
