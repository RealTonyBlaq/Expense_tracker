#!/usr/bin/python3
""" Expense Tracker Flask App """

from flask import Flask
from models import storage


app = Flask(__name__)


@app.teardown_appcontext
def shutdown(error=None):
    """ Closes a Database session """
    storage.
