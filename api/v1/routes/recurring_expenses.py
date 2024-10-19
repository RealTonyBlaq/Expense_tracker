#!/usr/bin/env python3
""" Recurring Expense Route """

from api.v1 import ETapp, date_format
from datetime import datetime
from dotenv import find_dotenv, load_dotenv
from flask import abort, jsonify, request
from flask_jwt_extended import get_current_user, jwt_required
from models.category import Category
from models.recurring_expense import RecurringExpense
from utilities import db
from werkzeug.exceptions import BadRequest


load_dotenv(find_dotenv())


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


@ETapp.route('/categories/<category_id>/recurring_expenses',
             methods=['POST'], strict_slashes=False)
@jwt_required()
def create_recurring(category_id):
    """ Creates a recurring expense object """
    current_user = get_current_user()
    if not current_user or not current_user.is_authenticated:
        abort(401)

    if request.is_json:
        try:
            data = request.get_json()
        except BadRequest:
            return jsonify(message='Error parsing JSON data'), 400

        category = db.query(Category).filter_by(id = category_id, user_id = current_user.id).first()
        if not category:
            abort(404)

        for key in ['amount', 'start_date', 'frequency']:
            if key not in data:
                return jsonify(message=f'{key} missing'), 400

        try:
            amount = float(data.get('amount'))
        except (ValueError, TypeError):
            return jsonify(message='Amount must be an integer/float'), 400

        end_date = data.get('end_date')

        try:
            start_date = datetime.strptime(data.get('start_date'), date_format)
            if end_date:
                end_date = datetime.strptime(end_date, date_format)
        except (ValueError, TypeError):
            return jsonify(message="Invalid date format. Please use 'YYYY-mm-dd'"), 400

        frequency = data.get('frequency').lower()
        if frequency not in ['daily', 'weekly', 'monthly']:
            return jsonify(message='Frequency must be daily, weekly or monthly'), 400

    return jsonify(message='Not a valid JSON'), 400
