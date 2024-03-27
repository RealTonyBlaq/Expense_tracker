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
        obj = storage.find(Category, )
