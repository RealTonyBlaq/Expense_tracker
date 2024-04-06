#!/usr/bin/python3
""" Extension of the Expense app that handles errors """


from api import ETapp
from flask import jsonify
from models.category import Category
from models.expense import Expense
from models.user import User
from models import storage


@ETapp.route('/stats', strict_slashes=False)
def stats():
    """ Returns a count of User, Category and Expense objects """
    obj_stats = {'users': len(storage.all(User)),
                 'categories': len(storage.all(Category)),
                 'expenses': len(storage.all(Expense))}
    return jsonify(obj_stats)


@ETapp.route('/status', strict_slashes=False)
def status():
    """ Returns a dict to show that the API is active """
    return jsonify({'status': 'Active'})
