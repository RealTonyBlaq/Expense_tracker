#!/usr/bin/env python3
""" Routes that manage User authentication """

from api.v1 import ETapp
from bcrypt import hashpw, checkpw, gensalt
from datetime import datetime
from dotenv import load_dotenv, find_dotenv
from flask import request, jsonify
from flask_jwt_extended import (create_access_token,
                                jwt_required, set_access_cookies,
                                get_current_user, unset_jwt_cookies)
from models.user import User
from os import getenv
import pyotp
from utilities import db, cache
from utilities.email import Email
from werkzeug.exceptions import BadRequest, BadRequestKeyError


load_dotenv(find_dotenv())


def hash_password(password):
    """ Returns a hashed password """
    return hashpw(password.encode('utf-8'), gensalt())


def generate_otp() -> str:
    """ Returns a 6 - digit token """
    secret = pyotp.random_base32()
    totp = pyotp.TOTP(secret)
    return totp.now()


try:
    OTP_TIMEOUT = int(getenv('OTP_TIMEOUT'))
except (ValueError, TypeError) as e:
    print('An error occurred: Invalid OTP_TIMEOUT env', e.args)
    exit(1)


@ETapp.route('/signup', methods=['POST'], strict_slashes=False)
def signup():
    """ Creates a User account """
    if request.is_json:
        try:
            data = request.get_json()
        except BadRequest:
            return jsonify(message='Error parsing JSON data'), 400

        for key in ['first_name', 'last_name', 'email', 'password',
                    'confirm_password']:
            if not data.get(key):
                return jsonify(message=f'{key} missing'), 400

        email = data.get('email').strip()
        first_name = data.get('first_name').strip()
        last_name = data.get('last_name').strip()
        password = data.get('password').strip()
        confirm_password = data.get('confirm_password').strip()

        # Checks if the user exists
        try:
            existing_user = db.get_user(email)
            return jsonify(message='user already exists'), 400
        except ValueError:
            pass

        # checks if both passwords match
        if password != confirm_password:
            return jsonify(message='password mismatch'), 400

        user_data = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'password': hash_password(password)
        }

        # create the user
        user = User(**user_data)
        OTP = generate_otp()
        user.save()

        if not Email.send_confirmation_email(user, OTP, OTP_TIMEOUT):
            return jsonify(message='An error occurred!'), 400

        # Cache the OTP with the user's email
        key = f'auth_{OTP}'
        cache.set(key, user.email, OTP_TIMEOUT)

        return jsonify(message='user created successfully. \
            Check your inbox for the OTP'), 201

    return jsonify(message='Not a valid JSON'), 400


@ETapp.route('/login', methods=['POST', 'GET'], strict_slashes=False)
def login():
    """ Logs a user in and creates a session"""
    if request.method == 'POST':
        if request.is_json:
            try:
                data = request.get_json()
            except BadRequest:
                return jsonify(message='Error parsing JSON data'), 400

            if not data.get('email'):
                return jsonify(message='email missing'), 400

            if not data.get('password'):
                return jsonify(message='password missing'), 400

            email = data.get('email').strip().lower()
            password = data.get('password').strip()

            try:
                user = db.get_user(email)
            except ValueError:
                return jsonify(message='User not found'), 404

            if not checkpw(password.encode('utf-8'), user.password):
                return jsonify(message="Incorrect password"), 401

            if not user.is_active:
                return jsonify(message='Please verify your email to \
                    login'), 401

            if user.is_2fa_enabled:
                OTP = generate_otp()

                if not Email.send_otp(user, OTP, OTP_TIMEOUT):
                    return jsonify(message='An error occurred. OTP send failure.'), 500
                # Cache the OTP
                key = f'auth_{OTP}'
                cache.set(key, user.email, OTP_TIMEOUT)
                return jsonify(message='OTP sent successfully'), 200

            access_token = create_access_token(identity=user)
            user.last_login_time = datetime.now()
            user.is_logged_in = True
            user.save()
            response = jsonify(message='login successful', user=user.to_dict())
            set_access_cookies(response, access_token)
            return response, 200

        return jsonify(message='Not a JSON'), 400


@ETapp.route('/logout', strict_slashes=False)
@jwt_required()
def logout():
    """ Logs a user out from the session """
    current_user = get_current_user()
    if not current_user or not current_user.is_authenticated:
        return jsonify(message='user not logged in'), 401

    current_user.is_logged_in = False
    current_user.save()

    response = jsonify(message='User logged out successfully')
    unset_jwt_cookies(response)
    return response, 200


@ETapp.route('/reset-password', methods=['POST', 'PATCH'],
             strict_slashes=False)
def reset():
    """ Resets a user's password """
    if request.method == 'PATCH':
        if request.is_json:
            try:
                data = request.get_json()
            except BadRequest:
                return jsonify(message='Error parsing JSON data'), 400

            for key in ['email', 'new_password', 'confirm_password', 'OTP']:
                if key not in data:
                    return jsonify(message=f'{key} missing'), 400

            email = data.get('email').lower().strip()
            new_password = data.get('new_password').strip()
            confirm_password = data.get('confirm_password').strip()
            OTP = data.get('OTP')

            key = f'auth_{OTP}'
            derived_email = cache.get(key)
            if not derived_email or derived_email != email:
                return jsonify(message='The OTP is invalid or expired'), 400

            if new_password != confirm_password:
                return jsonify(message='password mismatch'), 400

            try:
                existing_user = db.get_user(email)
            except ValueError:
                return jsonify(message='Invalid user email'), 400

            existing_user.password = hash_password(new_password)
            existing_user.save()
            cache.delete(key)
            return jsonify(message='Password changed successfully'), 200

        return jsonify(message='Not a valid JSON'), 400

    if request.method == 'POST':
        if request.is_json:
            try:
                data = request.get_json()
            except BadRequest:
                return jsonify(message='Error parsing JSON data'), 400

            # code to create a token and cache it for 5 minutes
            email = data.get('email')
            if not email:
                return jsonify(message='email missing'), 400

            try:
                user = db.get_user(email.lower().strip())
            except ValueError:
                return jsonify(message='User not found'), 400

            OTP = generate_otp()
            if not Email.send_otp(user, OTP, OTP_TIMEOUT):
                return jsonify(message='An error occurred. OTP send failure'), 400

            # Cache the OTP
            key = f'auth_{OTP}'
            cache.set(key, email, OTP_TIMEOUT)

            return jsonify(message='OTP sent. Please check your email inbox'), 200

        return jsonify(message='Not a Valid JSON'), 400


@ETapp.route('/resend_otp', strict_slashes=False)
def resend_otp():
    """ Resends OTP to the Email """
    email_by_param = request.args.get('email')
    process = request.args.get('process')
    if not email_by_param or not process:
        return jsonify(message='Email or process parameter missing'), 400

    try:
        user = db.get_user(email_by_param)
    except ValueError:
        return jsonify(message="user not found"), 404

    OTP = generate_otp()

    if process == 'signup':
        if user.is_email_verified:
            return jsonify(message='User email already verified'), 400

        if not Email.send_confirmation_email(user, OTP, OTP_TIMEOUT):
            return jsonify(message='An error occurred. OTP send failure!'), 400

        key = f'auth_{OTP}'
        cache.set(key, user.email, OTP_TIMEOUT)

        return jsonify(message='OTP resent successfully'), 200
    elif process == '2fa':
        if not user.is_2fa_enabled:
            return jsonify(message='Multi-authentication is not enabled'), 400

        if not Email.send_otp(user, OTP, OTP_TIMEOUT):
            return jsonify(message='An error occurred. OTP send failure'), 400

        # Cache the OTP
        key = f'auth_{OTP}'
        cache.set(key, user.email, OTP_TIMEOUT)
        return jsonify(message='OTP resent successfully'), 200

    return jsonify(message='Invalid process type'), 401


@ETapp.route('/auth/verify/<process>/<otp>',
             strict_slashes=False)
def verify_otp(process, otp):
    """ Route that verifies the OTP """
    key = f'auth_{otp}'
    email = cache.get(key)
    try:
        email_by_param = request.args['email']
    except BadRequestKeyError:
        return jsonify(message='Email parameter missing'), 400

    if not email or email != email_by_param:
        return jsonify(message='Invalid OTP, try again'), 400

    try:
        user = db.get_user(email)
    except ValueError:
        return jsonify(message='Invalid OTP, try again'), 400

    if process == 'signup':
        if user.is_email_verified:
            return jsonify(message='Email already verified'), 400

        user.is_email_verified = True
        user.save()
        cache.delete(key)
        return jsonify(message='Email verification successful'), 200
    elif process == '2fa':
        user.last_login_time = datetime.now()
        user.is_email_verified = True
        user.is_logged_in = True
        user.save()
        cache.delete(key)
        response = jsonify(message='login successful', user=user.to_dict())
        access_token = create_access_token(identity=user)
        set_access_cookies(response, access_token)
        return response, 200

    return jsonify(message='Invalid process type'), 401
