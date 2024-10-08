#!/usr/bin/env python3
""" The Category Route """

from api.v1 import ETapp
from flask import jsonify, abort, request
from flask_jwt_extended import jwt_required, get_current_user
from models.category import Category
from models.expense import Expense
from utilities import db


@ETapp.route('/categories', strict_slashes=False)
@ETapp.route('/categories/<category_id>', strict_slashes=False)
@jwt_required()
def get_categories(category_id=None):
    """ Returns a list of categories with the associating Expenses """
    current_user = get_current_user()
    if not current_user or not current_user.is_authenticated:
        return jsonify({'message': 'user not logged in'}), 401

    if category_id:
        category = db.query(Category).filter_by(id = category_id, user_id = current_user.id).first()
        if category is None:
            abort(404)

        data = category.to_dict()
        # associated_expenses = db.query(Expense).filter_by(category_id = category.id, user_id = current_user.id).all()
        # expenses = [ex.to_dict() for ex in associated_expenses]
        data['expenses'] = [expense.to_dict() for expense in category.expenses]

        return jsonify(message='success', data=data), 200

    all_category = db.query(Category).filter_by(user_id = current_user.id).all()
    data = []
    for cat in all_category:
        obj = cat.to_dict()
        obj['expenses'] = [e.to_dict() for e in cat.expenses]
        data.append(obj)

    return jsonify(message='success', data=data), 200


@ETapp.route('/categories', methods=['POST'], strict_slashes=False)
@jwt_required()
def create_category():
    """ Creates a new Category object """
