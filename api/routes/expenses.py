#!/usr/bin/python3
""" Expense route """

from api import ETapp
from flask import abort, jsonify, make_response, request
from Expense_tracker.models.income import Category
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
            if 'amount' not in data:
                abort(400, 'Missing expense amount')
            data['category_id'] = category_id
            expense = Expense(**data)
            expense.save()
            return make_response(jsonify(expense.about()), 201)
        abort(404)
    abort(400, "Not a JSON")


@ETapp.route('/expenses/<id>', methods=['PUT'])
def update_expense(id):
    """ Updates an expense object """
    if request.is_json is True:
        obj = storage.find(Expense, id)
        if obj:
            data = request.get_json()
            for key, value in data.items():
                if key not in ['id', 'created_at', 'updated_it',
                               'category_id']:
                    if 'decrease_by' in data and 'increase_by' in data:
                        abort(400, "Both increase_by and decrease_by \
                            cannot be in request data")
                    elif key == 'increase_by' and 'amount' not in data:
                        obj.increase_by(data['increase_by'])
                        continue
                    elif key == 'decrease_by' and 'amount' not in data:
                        obj.decrease_by(data['decrease_by'])
                        continue
                    setattr(obj, key, value)
            obj.save()
            return make_response(jsonify(obj.about()), 200)
        abort(404)
    abort(400, 'Not a JSON')
