#!/usr/bin/python3
""" The Category route """

from api import ETapp
from flask import abort, make_response, jsonify
from models.category import Category
from models import storage


@ETapp.route('/categories', strict_slashes=False)
@ETapp.route('/categories/<id>', strict_slashes=False)
def retrieve(id=None):
    if id:
        obj = storage.find(Category, id)
        if obj:
            return make_response(jsonify(obj.about()), 200)
        abort(404)
    else:
        categories = [obj.about() for obj in storage.all(Category).values()]
        return make_response(jsonify(categories), 200)


@ETapp.route('/categories/<id>', )
