#!/usr/bin/env python3
""" Recurring Expense Route """

from api.v1 import ETapp
from datetime import datetime
from flask import abort, jsonify
from flask_jwt_extended import get_current_user, jwt_required
from models.recurring_expense import RecurringExpense
from werkzeug.exceptions import BadRequest


@ETapp.route('/recurring_expenses', strict_slashes=False)
@ETapp.route('/recurring_expenses/<id')
