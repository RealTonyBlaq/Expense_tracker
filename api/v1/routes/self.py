#!/usr/bin/env python3
""" The current user route """

from api.v1 import ETapp
from api.v1.app import app
from api.v1.routes.auth import hash_password
from datetime import datetime
from flask import abort, jsonify, request
from flask_jwt_extended import jwt_required, get_current_user, unset_jwt_cookies
from models.user import User
from models.category import Category
from models.earning import Earning
from models.expense import Expense
from models.recurring_expense import RecurringExpense
from models.tag import Tag
import os
from utilities import db
from werkzeug.exceptions import BadRequest


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename: str) -> bool:
    """ Validates an uploaded file """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@ETapp.route('/me', methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
@jwt_required()
def get_me():
    """
    GET /me - Returns a JSON with the user information
    PATCH /me - Resets a user's password and other data
    DELETE /me - Deletes a user account
    """
    current_user = get_current_user()
    if not current_user or not current_user.is_authenticated:
        abort(401)

    if request.method == 'GET':
        user_dict = current_user.to_dict()
        user_dict['categories'] = [cat.to_dict() for cat in current_user.categories]
        user_dict['earnings'] = [e.to_dict() for e in current_user.earnings]
        user_dict['expenses'] = [ex.to_dict() for ex in current_user.expenses]
        user_dict['recurring_expenses'] = [rec.to_dict() for rec in current_user.recurring_expenses]
        user_dict['tags'] = [tag.to_dict() for tag in current_user.tags]

        return jsonify(message='success', data=user_dict), 200

    if request.method == 'PUT':
        if not request.is_json:
            return jsonify(message='Not a valid JSON'), 400

        try:
            data = request.get_json()
        except BadRequest:
            return jsonify(message='Error parsing JSON data'), 400

        update_data = {}
        if data.get('bio', None):
            update_data['bio'] = data.get('bio')

        if data.get('password', None):
            if not data.get('confirm_password'):
                return jsonify(message='confirm_password missing'), 400

            if data.get('password').strip() != data.get('confirm_password').strip():
                return jsonify(message='password mismatch'), 400

            update_data['password'] = hash_password(data.get('password').strip())

        if data.get('first_name', None):
            update_data['first_name'] = data.get('first_name').strip()

        if data.get('last_name', None):
            update_data['last_name'] = data.get('last_name').strip()

        for key, value in update_data.items():
            setattr(current_user, key, value)

        current_user.save()
        return jsonify(message='success', data=current_user.to_dict()), 200

    if request.method == 'DELETE':
        current_user.delete()
        response = jsonify(message='success')
        unset_jwt_cookies(response)
        return response, 200


@ETapp.route('/upload-avatar', methods=['POST'], strict_slashes=False)
@jwt_required()
def post_profile_picture():
    """ Handles Picture upload """
    current_user = get_current_user()
    if not current_user or not current_user.is_authenticated:
        abort(401)

    if 'image' not in request.files:
        return jsonify(message='No image found in the request'), 400

    file = request.files['image']
    if not file or file.filename == '':
        return jsonify(message='No file selected'), 400

    if allowed_file(file.filename):
        file_ext = file.filename.rsplit('.', 1)[1]
        filename = f'User{current_user.id}.{file_ext}'
        filepath = os.path.join(app.config['UPLOADS_FOLDER'], filename)
        file.save(filepath)
        return jsonify(message='')
