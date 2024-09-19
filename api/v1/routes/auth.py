#!/usr/bin/env python3
""" Routes that manage User authentication """

from api.v1 import ETapp
from bcrypt import hashpw, checkpw, gensalt
from datetime import datetime
from flask import request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from models.user import User
from random import randint
from utilities import db, cache
from utilities.email import Email


def hash_password(password):
    """ Returns a hashed password """
    return hashpw(password.encode('utf-8'), gensalt())


def generate_otp() -> int:
    """ Returns a 6 - digit token """
    return randint(100000, 999999)


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
        key = f'auth_{OTP}'
        cache.set(key, user.email, 300.00)
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

        Kindly note that OTP expires after 5 minutes.

        By verifying your email address, you'll gain access to the site.

        If you did not register for an account with WeBlog, \
        please ignore this email.

        Thank you for joining us!

        Best regards,
        The Expense Tracker Team"""

        Email.send(user.email, subject, content)
        return jsonify({'message': 'user created successfully'}), 201

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

            if not user.is_active:
                return jsonify({'message': 'Please verify your email to login'}), 401

            if not checkpw(password.encode('utf-8'), user.password):
                return jsonify({"message": "Incorrect password"})

            if login_user(user=user):
                user.last_login_time = datetime.now()
                user.is_logged_in = True
                user.save()
                return jsonify({'message': 'login successful', 'user': user.to_dict()}), 200

            return jsonify({'message': 'Please verify your email to login'})

        return jsonify({'message': 'Not a JSON'}), 400


@ETapp.route('/logout', strict_slashes=False)
@login_required
def logout():
    """ Logs a user out from the session """
    if not current_user.is_authenticated:
        return jsonify({'message': 'user not logged in'}), 401

    current_user.is_logged_in = False
    current_user.save()
    logout_user()

    return jsonify({'message': 'User logged out successfully'}), 200


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
            OTP = data.get('token')

            key = 'auth_{OTP}'
            derived_email = cache.get(key)
            if not derived_email or derived_email != email:
            try:
                existing_user = db.get_user(email)
            except ValueError:
                return jsonify({'message': 'Invalid user email'}), 400

            if new_password != confirm_password:
                return jsonify({'message': 'password mismatch'}), 400

            existing_user.password = hash_password(new_password)
            existing_user.save()
            return jsonify({'message': 'Password changed successfully'}), 200

        return jsonify({'message': 'Not a valid JSON'}), 400

    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()

            # code to create a token and cache it for 5 minutes
        return jsonify({'message': 'Not a Valid JSON'}), 400
