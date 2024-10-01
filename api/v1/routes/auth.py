#!/usr/bin/env python3
""" Routes that manage User authentication """

from api.v1 import ETapp
from bcrypt import hashpw, checkpw, gensalt
from datetime import datetime
from dotenv import load_dotenv, find_dotenv
from flask import request, jsonify
from flask_login import login_user, current_user
from flask_jwt_extended import (create_access_token, get_jwt_identity,
                                jwt_required, set_access_cookies,
                                current_user, unset_jwt_cookies)
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


OTP_TIMEOUT = int(getenv('OTP_TIMEOUT'))


@ETapp.route('/signup', methods=['POST'], strict_slashes=False)
def signup():
    """ Creates a User account """
    if request.is_json:
        data = request.get_json()
        for key in ['first_name', 'last_name', 'email', 'password', 'confirm_password']:
            if not data.get(key):
                return jsonify({'message': f'{key} missing'}), 400

        email = data.get('email').strip()
        first_name = data.get('first_name').strip()
        last_name = data.get('last_name').strip()
        password = data.get('password').strip()
        confirm_password = data.get('confirm_password').strip()

        # Checks if the user exists
        try:
            existing_user = db.get_user(email)
            return jsonify({'message': 'user already exists'}), 400
        except ValueError:
            pass

        # checks if both passwords match
        if password != confirm_password:
            return jsonify({'message': 'password mismatch'}), 400

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

        subject = "Expense Tracker - Welcome | OTP"
        content = f"""Dear {user.first_name} {user.last_name},

        Thank you for registering with Expense Tracker! To complete your \
        registration, please verify your email address using the OTP below:

        <div style="justify-content: space-around;">

        <h1 style="display: inline-block; padding: \
        10px 20px; background-color: #007bff; color: #fff; text-decoration: \
        none; border-radius: 5px; position: absolute;">{OTP}</h1>

        </div>

        Kindly note that OTP expires after {OTP_TIMEOUT} minutes.

        By verifying your email address, you'll gain access to the site.

        If you did not register for an account with Expense Tracker, \
        please ignore this email.

        Thank you for joining us!

        Best regards,
        The Expense Tracker Team"""

        Email.send(user.email, subject, content)
        # Cache the OTP with the user's email
        key = f'auth_{OTP}'
        cache.set(key, user.email, OTP_TIMEOUT)

        return jsonify({'message': 'user created successfully. Check your inbox for the OTP'}), 201

    return jsonify({'message': 'Not a valid JSON'}), 400


@ETapp.route('/login', methods=['POST', 'GET'], strict_slashes=False)
def login():
    """ Logs a user in and creates a session"""
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()

            if not data.get('email'):
                return jsonify({'message': 'email missing'}), 400

            if not data.get('password'):
                return jsonify({'message': 'password missing'}), 400

            email = data.get('email').strip()
            password = data.get('password').strip()

            try:
                user = db.get_user(email)
            except ValueError:
                return jsonify({'message': 'User not found'}), 404

            if not checkpw(password.encode('utf-8'), user.password):
                return jsonify({"message": "Incorrect password"}), 401

            if not user.is_active:
                return jsonify({'message': 'Please verify your email to login'}), 401

            if user.is_2fa_enabled:
                OTP = generate_otp()

                subject = "Expense Tracker - Reset Password | OTP"
                content = f"""Dear {user.first_name} {user.last_name},

                You just tried to log in to your account. Please authenticate \
                your login session using the OTP below:

                <div style="justify-content: space-around;">

                <h1 style="display: inline-block; padding: \
                10px 20px; background-color: #007bff; color: #fff; text-decoration: \
                none; border-radius: 5px; position: absolute;">{OTP}</h1>

                </div>

                OTP expires after {OTP_TIMEOUT} minutes.

                If you did not initiate a login attempt, please ignore this email or contact us.

                Thank you!

                Best regards,
                The Expense Tracker Team"""

                Email.send(user.email, subject, content)
                # Cache the OTP
                key = f'auth_{OTP}'
                cache.set(key, user.email, OTP_TIMEOUT)
                return jsonify({'message': 'OTP sent successfully'}), 200

            access_token = create_access_token(identity=user)
            user.last_login_time = datetime.now()
            user.is_logged_in = True
            user.save()
            response = jsonify({'message': 'login successful', 'user': user.to_dict()}), 200
            set_access_cookies(response, access_token)
            return response, 200

        return jsonify({'message': 'Not a JSON'}), 400


@ETapp.route('/logout', strict_slashes=False)
@jwt_required()
def logout():
    """ Logs a user out from the session """
    if not current_user.is_authenticated:
        return jsonify({'message': 'user not logged in'}), 401

    current_user.is_logged_in = False
    current_user.save()

    response = jsonify({'message': 'User logged out successfully'})
    unset_jwt_cookies(response)
    return response, 200


@ETapp.route('/reset-password', methods=['POST', 'PATCH'],
             strict_slashes=False)
def reset():
    """ Resets a user's password """
    if request.method == 'PATCH':
        if request.is_json:
            data = request.get_json()
            for key in ['email', 'new_password', 'confirm_password', 'OTP']:
                if key not in data:
                    return jsonify({'message': f'{key} missing'}), 400

            email = data.get('email').lower()
            new_password = data.get('new_password')
            confirm_password = data.get('confirm_password')
            OTP = data.get('OTP')

            key = f'auth_{OTP}'
            derived_email = cache.get(key)
            if not derived_email or derived_email != email:
                return jsonify({'message': 'The OTP is invalid or expired'}), 400

            if new_password != confirm_password:
                return jsonify({'message': 'password mismatch'}), 400

            try:
                existing_user = db.get_user(email)
            except ValueError:
                return jsonify({'message': 'Invalid user email'}), 400

            existing_user.password = hash_password(new_password)
            existing_user.save()
            cache.delete(key)
            return jsonify({'message': 'Password changed successfully'}), 200

        return jsonify({'message': 'Not a valid JSON'}), 400

    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()

            # code to create a token and cache it for 5 minutes
            email = data.get('email')
            if not email:
                return jsonify({'message': 'email missing'}), 400

            try:
                user = db.get_user(email.lower())
            except ValueError:
                return jsonify({'message': 'User not found'}), 400

            OTP = generate_otp()

            subject = "Expense Tracker - Reset Password | OTP"
            content = f"""Dear {user.first_name} {user.last_name},

            Authenticate your password reset using the OTP below:

            <div style="justify-content: space-around;">

            <h1 style="display: inline-block; padding: \
            10px 20px; background-color: #007bff; color: #fff; text-decoration: \
            none; border-radius: 5px; position: absolute;">{OTP}</h1>

            </div>

            OTP expires after {OTP_TIMEOUT} minutes.

            If you did not initiate a password reset, please ignore this email.

            Thank you!

            Best regards,
            The Expense Tracker Team"""

            Email.send(user.email, subject, content)
            # Cache the OTP
            key = f'auth_{OTP}'
            cache.set(key, email, OTP_TIMEOUT)

            return jsonify({'message', 'OTP sent. Please check your email inbox'}), 200

        return jsonify({'message': 'Not a Valid JSON'}), 400


@ETapp.route('/resend_otp/<process>', strict_slashes=False)
def resend_otp(process):
    """ Resends OTP to the Email """
    try:
        email_by_param = request.args['email']
    except BadRequestKeyError:
        return jsonify(message='Email parameter missing'), 400

    try:
        user = db.get_user(email_by_param)
    except ValueError:
        return jsonify(message="user not found"), 404

    OTP = generate_otp()

    if process == 'signup':
        if user.is_email_verified:
            return jsonify(message='User email already verified'), 400

        subject = "Expense Tracker - Reset Password | OTP"
        content = f"""Dear {user.first_name} {user.last_name},

        You just tried to log in to your account. Please authenticate \
        your login session using the OTP below:

        <div style="justify-content: space-around;">

        <h1 style="display: inline-block; padding: \
        10px 20px; background-color: #007bff; color: #fff; text-decoration: \
        none; border-radius: 5px; position: absolute;">{OTP}</h1>

        </div>

        OTP expires after {OTP_TIMEOUT} minutes.

        If you did not initiate a login attempt, please ignore this email or contact us.

        Thank you!

        Best regards,
        The Expense Tracker Team"""

        Email.send(user.email, subject, content)


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
        return jsonify({'message': 'Invalid OTP, try again'}), 400

    try:
        user = db.get_user(email)
    except ValueError:
        return jsonify({'message': 'Invalid OTP, try again'}), 400

    if process == 'signup':
        if user.is_email_verified:
            return jsonify({'message': 'Email already verified'}), 400
        user.is_email_verified = True
        user.save()
        cache.delete(key)
        return jsonify({'message': 'Email verification successful'}), 200
    elif process == '2fa':
        user.last_login_time = datetime.now()
        user.save()
        cache.delete(key)
        response = jsonify({'message': 'login successful', 'user': user.to_dict()})
        access_token = create_access_token(identity=user)
        set_access_cookies(response, access_token)
        return response, 200

    return jsonify({'message': 'Invalid process type'}), 401
