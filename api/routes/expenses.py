#!/usr/bin/python3
""" Expense route """

from api import ETapp
from flask import abort, jsonify, make_response, request
from models.category import Category
from models.expense import Expense
from models import storage


@ETapp.route('/expenses', strict_slashes=False)
@ETapp.route('/expenses/<id>', strict_slashes=False)
def retrieve_expense(id=None):
    """ Returns a dict/list of expense objects using the about() method """
    if id:
        obj = storage.find(Expense, id)
        if obj:
            return make_response(jsonify(obj.about()), 200)
        abort(404)
    else:
        objs = []
