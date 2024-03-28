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
        expenses = [obj.about() for obj in storage.all(Expense).values()]
        return make_response(jsonify(expenses), 200)


@ETapp.route('/expenses/<id>', methods=['DELETE'],
             strict_slashes=False)
def del_expense(id):
    """ Deletes an expense obj from storage """
    obj = storage.find(Expense, id)
    if obj:
        storage.delete(obj)
        return make_response(jsonify({}), 200)
    abort(404)


@ETapp.route('/categories/<category_id>/expenses', methods=['POST'],
             strict_slashes=False)
def create_expense(category_id):
    """ Creates a new expense obj based on Category """
    if request.is_json is True:
        category = storage.find(Category, category_id)
        if category:
            data = request.get_json()
            
