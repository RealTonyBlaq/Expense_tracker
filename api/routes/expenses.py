#!/usr/bin/python3
""" Expense route """

from api import ETapp
from flask import abort, jsonify, make_response, request
from models.category import Category
from models.expense import Expense
from models import storage


@ETapp.route('/expenses', strict_slashes=False)
r
