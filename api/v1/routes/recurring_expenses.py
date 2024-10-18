#!/usr/bin/env python3
""" Recurring Expense Route """

from api.v1 import ETapp
from datetime import datetime
from flask import abort, jsonify
from flask_jwt_extended import get_current_user, jwt_required
from models.recurring_expense import RecurringExpense
from utilities import db
from werkzeug.exceptions import BadRequest


@ETapp.route('/recurring_expenses', strict_slashes=False)
@ETapp.route('/recurring_expenses/<id>', strict_slashes=False)
@jwt_required()
def get_recurring_expense(id=None):
    """ Returns the current_user's recurring expenses """
    current_user = get_current_user()
    if not current_user or not current_user.is_authenticated:
        abort(401)

    if id:
        
