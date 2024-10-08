#!/usr/bin/env python3
""" The Category Route """

from api.v1 import ETapp
from flask import jsonify, abort
from flask_jwt_extended import jwt_required, get_current_user
from models.category import Category
from models.expense import Expense
from utilities import db


@ETapp.route('/categories', strict_slashes=False)
@ETapp.route('/categories/<category_id>', strict_slashes=False)
@jwt_required()
def get_categories(category_id):
    """ Returns a list of categories with the associating Expenses """
    current_user = get_current_user()
    if not current_user or not current_user.is_authenticated:
        return jsonify({'message': 'user not logged in'}), 401

    if category_id:
        category = db.query(Category).filter_by(id = category_id, user_id = current_user.id).first()
        if category is None:
            return jsonify(message='Invalid category'), 400
        data = category.to_dict()
        associated_expenses = db.query(Expense).filter_by(category_id = category.id, user_id = current_user.id).all()
        expenses = [ex.to_dict() for ex in associated_expenses]
