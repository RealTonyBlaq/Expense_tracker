#!/usr/bin/python3
""" Expense Tracker Flask App """

from flask import Flask


app = Flask(__name__)


@app.teardown_appcontext
def shutdown(error=None):
    
