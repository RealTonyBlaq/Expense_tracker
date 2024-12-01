#!/usr/bin/env python3
""" The current user route """

from api.v1 import ETapp
from api.v1.routes.auth import hash_password
from bcrypt import checkpw
from datetime import datetime
from flask import abort, jsonify, request
from flask_jwt_extended import jwt_required, get_current_user, unset_jwt_cookies
from utilities.email import Email
from werkzeug.exceptions import BadRequest


@ETapp.route('/me', methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
@jwt_required()
def get_me():
    """
    GET /me - Returns a JSON with the user information
    PUT /me - Resets a user's password and other data
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


@ETapp.route('/me/statement', methods=['GET'], strict_slashes=False)
@jwt_required()
def my_statement():
    """ Sends an email to the user containing their expense statement """
    current_user = get_current_user()
    if not current_user or not current_user.is_authenticated:
        abort(401)

    if not current_user.is_active:
        return jsonify(message='Please verify your email first.'), 403

    if not Email.send_statement(current_user):
        return jsonify(message='An error occurred. Statement could not be generated.'), 400

    return jsonify(message='Statement sent successfully! Please check your inbox.'), 200


@ETapp.route('/me/enable_2fa', methods=['POST'],
             strict_slashes=False)
@jwt_required()
def enable_2fa():
    """
    POST /me/enable_2fa
        Activates another level of security for the user
        that sends OTP to the registered at every log in attempt
    """
    current_user = get_current_user()
    if not current_user or not current_user.is_authenticated:
        abort(401)

    if not request.is_json:
        return jsonify(message='Not a valid JSON'), 400

    try:
        data = request.get_json()
    except BadRequest:
        return jsonify(message='Error parsing JSON data'), 400

    password = data.get('password')
    if not password:
        return jsonify(message='password missing'), 400

    if not checkpw(password.encode('utf-8'), current_user.password):
        return jsonify(message='Incorrect password'), 400

    current_user.is_2fa_enabled = True
    current_user.save()
    return jsonify
