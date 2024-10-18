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
        recurring_expense = db.query(RecurringExpense).filter_by(id = id, user_id = current_user.id).first()
        if recurring_expense:
            return jsonify(message='success', data=recurring_expense.to_dict()), 200
        abort(404)

    rec_expenses = db.query(RecurringExpense).filter_by(user_id = current_user.id).all()
    all_recurring = [e.to_dict() for e in rec_expenses]
    return jsonify(message='success', data=all_recurring), 200


@
