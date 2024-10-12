#!/usr/bin/env python3
""" The Expense Route """

from api.v1 import ETapp
from datetime import datetime
from dotenv import load_dotenv, find_dotenv
from models.category import Category
from models.expense import Expense
from flask import abort, jsonify, request
from flask_jwt_extended import get_current_user, jwt_required
from utilities import cache, db
from werkzeug.exceptions import BadRequest, BadRequestKeyError


date_format = "%Y-%m-%d"
load_dotenv(find_dotenv())


@ETapp.route('/expenses', sstrict_slashes=False)
@ETapp.route('/expenses/<expense_id>', strict_slashes=False)
@jwt_required()
def get_expenses(expense_id=None):
    """ Retrieves a JSON representation of expense objects """
    current_user = get_current_user()
    if not current_user or not current_user.is_authenticated:
        abort(401)

    if expense_id:
        expense = db.query(Expense).filter_by(id = expense_id, user_id = current_user.id).first()
        if expense:
            return jsonify(message='success', data=expense.to_dict()), 200
        abort(404)

    all_expenses = db.query(Expense).filter_by(user_id = current_user.id).all()
    expenses = [ex.to_dict for ex in all_expenses]
    return jsonify(message='success', data=expenses), 200


@ETapp.route('/categories/<category_id>/expenses', methods=['POST'],
             strict_slashes=False)
@jwt_required()
def create_expense(category_id):
    """ Creates a new Expense object """
    current_user = get_current_user()
    if not current_user or not current_user.is_authenticated:
        abort(401)

    if request.is_json:
        try:
            data = request.get_json()
        except BadRequest:
            return jsonify(message='Error parsing JSON data'), 400

        if 'amount' not in data:
            return jsonify(message='amount missing'), 400

        if 'date_occurred' not in data:
            return jsonify(message='date_occurred missing'), 400

        try:
            amount = int(data.get('amount'))
        except (ValueError, TypeError):
            return jsonify(message='Amount must be an integer'), 400

        try:
            date_occurred = datetime.strptime(data.get('date_occurred'), date_format)
        except (ValueError, TypeError) as e:
            return jsonify(message="Invalid date format. Please use '%Y-%m-%d'"), 400
    return jsonify(message='Not a valid JSON'), 400
