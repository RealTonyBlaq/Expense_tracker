#!/usr/bin/python3
""" Expense Tracker Flask App """

from api import ETapp
from flask import Flask, jsonify
from models import storage


app = Flask(__name__)
app.register_blueprint(ETapp)


@app.teardown_appcontext
def shutdown(error=None):
    """ Closes a Database session """
    storage.close()


@app.errorhandler(404)
def not_found():
    """ Returns a JSON if a request route wasn't found """
    return jsonify({'error': 'Not Found'})





if __name__ == '__main__':
    app.run('0.0.0.0', 5000)
