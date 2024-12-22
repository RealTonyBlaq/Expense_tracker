#!/usr/bin/env python3
""" The Category Route """

from api.v1 import ETapp
from dotenv import load_dotenv, find_dotenv
from flask import jsonify, abort, request
from flask_jwt_extended import jwt_required, get_current_user
from models.category import Category
from utilities import db
from werkzeug.exceptions import BadRequest


load_dotenv(find_dotenv())


@ETapp.route('/categories', strict_slashes=False)
@ETapp.route('/categories/<category_id>', strict_slashes=False)
@jwt_required()
def get_categories(category_id=None):
    """ Returns a list of categories with the associating Expenses """
    current_user = get_current_user()
    if not current_user or not current_user.is_authenticated:
        abort(401)

    if category_id:
        category = db.query(Category).filter_by(id=category_id,
                                                user_id=current_user.id).first()
        if category is None:
            abort(404)

        data = category.to_dict()
        data['expenses'] = [expense.to_dict() for expense in category.expenses]
        data['recurring_expenses'] = [rec.to_dict() for rec in
                                      category.recurring_expenses]

        return jsonify(message='success', data=data), 200

    data = []
    for cat in current_user.categories:
        obj = cat.to_dict()
        obj['expenses'] = [e.to_dict() for e in cat.expenses]
        obj['recurring_expenses'] = [rec.to_dict() for rec in
                                     cat.recurring_expenses]
        data.append(obj)

    return jsonify(message='success', data=data), 200


@ETapp.route('/categories', methods=['POST'], strict_slashes=False)
@jwt_required()
def create_category():
    """ Creates a new Category object """
    current_user = get_current_user()
    if not current_user or not current_user.is_authenticated:
        abort(401)

    if request.is_json:
        try:
            data = request.get_json()
        except BadRequest:
            return jsonify(message='Error parsing JSON data'), 400

        name = data.get("name").strip()
        if not name:
            return jsonify(message='Category name missing'), 400

        new_category = Category(name=name, user_id=current_user.id)
        new_category.save()

        return jsonify(message='success', data=new_category.to_dict()), 201

    return jsonify(message='Not a valid JSON'), 400


@ETapp.route('/categories/<category_id>', methods=['DELETE'],
             strict_slashes=False)
@jwt_required()
def delete_category(category_id):
    """ Deletes a user-created category from storage """
    current_user = get_current_user()
    if not current_user or not current_user.is_authenticated:
        abort(401)

    category_obj = db.query(Category).filter_by(
        id=category_id,
        user_id=current_user.id).first()
    if category_obj is None:
        abort(404)

    category_obj.delete()
    return jsonify(message='success'), 200


@ETapp.route('/categories/<category_id>', methods=['PUT'], strict_slashes=False)
@jwt_required()
def update_category(category_id):
    """ Updates a category object with data """
    current_user = get_current_user()
    if not current_user or not current_user.is_authenticated:
        abort(401)

    if not request.is_json:
        return jsonify(message='Not a valid JSON'), 400

    try:
        data = request.get_json()
    except BadRequest:
        return jsonify(message='Error parsing JSON data'), 400

    category_obj = db.query(Category).filter_by(id = category_id, user_id = current_user.id).first()
    if category_obj:
        name = data.get('name').strip()
        if name:
            setattr(category_obj, 'name', name)
            category_obj.save()
    else:
        abort(404)

    updated_data = category_obj.to_dict()
    updated_data['expenses'] = [e.to_dict() for e in category_obj.expenses]
    updated_data['recurring_expenses'] = [rec.to_dict() for rec in category_obj.recurring_expenses]

    return jsonify(message='success', data=updated_data), 200
