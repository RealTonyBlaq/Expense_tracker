#!/usr/bin/python3
""" Expense Tracker Flask App """

from flask import Flask
from models import storage


app = Flask(__name__)


@app.teardown_appcontext
def shutdown(error=None):
    """ Closes a Database session """
    storage.close()

@app.errorhandler(404)
def not_found():
    """ Returns a JSON if a"""
