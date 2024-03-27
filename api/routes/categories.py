#!/usr/bin/python3
""" The Category route """

from api import ETapp
from flask import abort, jsonify, make_response, request
from models.category import Category
from models import storage
from models.user import User


@ETapp.route('/categories', strict_slashes=False)
@ETapp.route('/categories/<id>', strict_slashes=False)
def retrieve(id=None):
    """ Retrieves a category object(s) from the database """
    if id:
        obj = storage.find(Category, id)
        if obj:
            return make_response(jsonify(obj.about()), 200)
        abort(404)
    else:
        categories = [obj.about() for obj in storage.all(Category).values()]
        return make_response(jsonify(categories), 200)


@ETapp.route('/categories/<id>', methods=['DELETE'],
             strict_slashes=False)
def delete(id):
    """ Deletes an object if it exists """
    obj = storage.find(Category, id)
    if obj:
        storage.delete(obj)
        return make_response(jsonify({}), 200)
    abort(404)


@ETapp.route('/users/<user_id>/categories/', methods=['POST'],
             strict_slashes=False)
def create(user_id):
    """ Creates a category obj if the user_id passed is valid """
    if request.is_json is True:
        if storage.find(User, user_id):
            data = request.get_json()
            if 'name' not in data:
                abort(400, 'Missing name')
            data['user_id'] = user_id
            category = Category(**data)
            category.save()
            return 
