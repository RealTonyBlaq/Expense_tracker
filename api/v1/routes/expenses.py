#!/usr/bin/env python3
""" The Expense Route """

from api.v1 import ETapp, date_format
from datetime import datetime
from dotenv import load_dotenv, find_dotenv
from models.category import Category
from models.expense import Expense
from flask import abort, jsonify, request
from flask_jwt_extended import get_current_user, jwt_required
from utilities import db
from werkzeug.exceptions import BadRequest


load_dotenv(find_dotenv())


@ETapp.route('/expenses', strict_slashes=False)
@ETapp.route('/expenses/<expense_id>', strict_slashes=False)
@jwt_required()
def get_expenses(expense_id=None):
    """ Retrieves a JSON representation of expense objects """
    current_user = get_current_user()
    if not current_user or not current_user.is_authenticated:
        abort(401)

    if expense_id:
        expense = db.query(Expense).filter_by(
            id=expense_id, user_id=current_user.id).first()
        if expense:
            return jsonify(message='success', data=expense.to_dict()), 200
        abort(404)

    all_expenses = db.query(Expense).filter_by(user_id=current_user.id).all()
    my_expenses = [ex.to_dict() for ex in all_expenses]
    return jsonify(message='success', data=my_expenses), 200


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

        category = db.query(Category).filter_by(
            id=category_id, user_id=current_user.id).first()
        if not category:
            return jsonify(message='Invalid category'), 400

        if 'amount' not in data:
            return jsonify(message='amount missing'), 400

        if 'date_occurred' not in data:
            return jsonify(message='date_occurred missing'), 400

        try:
            amount = float(data.get('amount'))
        except (ValueError, TypeError):
            return jsonify(message='Amount must be an integer/float'), 400

        try:
            date_occurred = datetime.strptime(data.get('date_occurred'),
                                              date_format)
        except (ValueError, TypeError):
            return jsonify(message="Invalid date format. \
                Please use 'YYYY-mm-dd'"), 400

        if date_occurred > datetime.today():
            return jsonify(message=f'{data["date_occurred"]} is in the \
                future. Use a valid date'), 400

        description = data.get('description')

        # Create the expense
        new_expense = Expense(category_id=category_id,
                              user_id=current_user.id,
                              amount=amount,
                              date_occurred=date_occurred,
                              description=description)
        new_expense.save()
        return jsonify(message='success', data=new_expense.to_dict()), 201

    return jsonify(message='Not a valid JSON'), 400


@ETapp.route('/expenses/<expense_id>', methods=['DELETE'],
             strict_slashes=False)
@jwt_required()
def delete_expense(expense_id):
    """ Deletes an Expense object if it exists """
    current_user = get_current_user()
    if not current_user or not current_user.is_authenticated:
        abort(401)

    my_expense = db.query(Expense).filter_by(id = expense_id, user_id = current_user.id).first()
    if my_expense:
        my_expense.delete()
        return jsonify(message='success'), 200

    abort(404)


@ETapp.route('/expenses/<expense_id>', methods=['PUT'],
             strict_slashes=False)
@jwt_required()
def update_expense(expense_id):
    """ Updates an expense object """
    current_user = get_current_user()
    if not current_user or not current_user.is_authenticated:
        abort(401)

    if request.is_json:
        try:
            data = request.get_json()
        except BadRequest:
            return jsonify(message='Error parsing JSON data'), 400

        my_expense = db.query(Expense).filter_by(id = expense_id, user_id = current_user.id).first()
        if not my_expense:
            abort(400)

        if 'amount' in data:
            try:
                data['amount'] = float(data.get('amount'))
            except (ValueError, TypeError):
                return jsonify(message='Amount must be an integer/float'), 400

        if 'date_occurred' in data:
            date_occurred = data['date_occurred']
            try:
                data['date_occurred'] = datetime.strptime(date_occurred, date_format)
            except (ValueError, TypeError):
                return jsonify(message="Invalid date format. Please use 'YYYY-mm-dd'"), 400

            if data['date_occurred'] > datetime.today():
                return jsonify(message=f'{data["date_occurred"]} is in the future. Use a valid date'), 400

        for key, value in data.items():
            if key in ['date_occurred', 'amount', 'description']:
                setattr(my_expense, key, value)

        my_expense.save()
        return jsonify(message='success', data=my_expense.to_dict()), 200

    return jsonify(message='Not a valid JSON'), 400
