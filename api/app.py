#!/usr/bin/python3
""" Expense Tracker Flask App """

from api import ETapp
from flask import Flask, jsonify
from Expense_tracker.models.income import Category
from models.expense import Expense
from models import storage
from models.user import User
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(ETapp)
CORS(app)


@app.teardown_appcontext
def shutdown(error=None):
    """ Closes a Database session """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ Returns a JSON if a request route wasn't found """
    return jsonify({'error': 'Not Found'})


@app.route('/api/stats', strict_slashes=False)
def stats():
    """ Returns a count of User, Category and Expense objects """
    obj_stats = {'users': len(storage.all(User)),
                 'categories': len(storage.all(Category)),
                 'expenses': len(storage.all(Expense))}
    return jsonify(obj_stats)


@app.route('/api/status', strict_slashes=False)
def status():
    """ Returns a dict to show that the API is active """
    return jsonify({'status': 'Active'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
