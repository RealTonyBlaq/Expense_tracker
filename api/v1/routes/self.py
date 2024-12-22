#!/usr/bin/env python3
""" The current user route """

from api.v1 import ETapp, date_format
from api.v1.routes.auth import hash_password
from bcrypt import checkpw
from datetime import datetime
from flask import abort, jsonify, request
from flask_jwt_extended import (jwt_required, get_current_user,
                                unset_jwt_cookies)
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
        user_dict['categories'] = [cat.to_dict() for cat in
                                   current_user.categories]
        user_dict['earnings'] = [e.to_dict() for e in current_user.earnings]
        user_dict['expenses'] = [ex.to_dict() for ex in current_user.expenses]
        user_dict['recurring_expenses'] = [rec.to_dict() for rec in
                                           current_user.recurring_expenses]
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

        if data.get('phone'):
            phone = data.get('phone')
            if len(phone) < 11:
                return jsonify(message='Invalid phone number'), 400
            update_data['phone'] = phone

        if data.get('password', None):
            if not data.get('confirm_password'):
                return jsonify(message='confirm_password missing'), 400

            if data['password'].strip() != data['confirm_password'].strip():
                return jsonify(message='password mismatch'), 400

            update_data['password'] = hash_password(data['password'].strip())

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

    start = request.args.get('from')
    end = request.args.get('to')

    if start is None:
        return jsonify(message='"from" date parameter is missing'), 400

    if end is None:
        return jsonify(message='"from" date parameter is invalid'), 400

    try:
        start_date = datetime.strptime(start, date_format)
        end_date = datetime.strptime(end, date_format)
    except (ValueError, TypeError):
        return jsonify(message="Invalid date format. \
            Please use 'YYYY-mm-dd'"), 400

    if start_date > end_date:
        return jsonify(message='"from" date should not be higher \
            than "to" date'), 400

    period = {'from': start_date, 'to': end_date}

    if not Email.send_statement(current_user, period):
        return jsonify(message='An error occurred. \
            Statement could not be generated.'), 400

    return jsonify(message='Statement sent successfully! \
        Please check your inbox.'), 200


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

    if current_user.is_2fa_enabled:
        return jsonify(message='Two-Factor Authentication \
            already enabled'), 200

    current_user.is_2fa_enabled = True
    current_user.save()
    return jsonify(message='Two Factor Authentication enabled \
        successfully'), 201


@ETapp.route('/me/disable_2fa', methods=['POST'],
             strict_slashes=False)
@jwt_required()
def disable_2fa():
    """
    POST /me/disable_2fa
        Disables Two-Factor Authentication for the User
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

    if not current_user.is_2fa_enabled:
        return jsonify(message='Two-Factor Authentication already disabled'), 200

    current_user.is_2fa_enabled = False
    current_user.save()
    return jsonify(message='Two-Factor Authentication \
        disabled successfully'), 200
