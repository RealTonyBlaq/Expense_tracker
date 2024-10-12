#!/usr/bin/env python3
""" The Earning route """

from api.v1 import ETapp
from datetime import datetime
from dotenv import load_dotenv, find_dotenv
from flask import abort, request, jsonify
from flask_jwt_extended import jwt_required, get_current_user
from models.earning import Earning
from utilities import db
from werkzeug.exceptions import BadRequest


date_format = "%Y-%m-%d"
load_dotenv(find_dotenv())


@ETapp.route('/earnings', strict_slashes=False)
@ETapp.route('/earnings/<earning_id>', strict_slashes=False)
@jwt_required()
def get_earnings(earning_id=None):
    """ Returns an object containing a list of Earning objects """
    current_user = get_current_user()
    if not current_user or not current_user.is_authenticated:
        abort(401)

    if earning_id:
        earning = db.query(Earning).filter_by(id = earning_id, user_id = current_user.id).first()
        if earning is not None:
            return jsonify(message='success', data=earning.to_dict()), 200
        abort(404)

    all_earnings = db.all(Earning).values()
    my_earnings = []
    for earning in all_earnings:
        if earning.user_id == current_user.id:
            my_earnings.append(earning.to_dict())

    return jsonify(message='success', data=my_earnings), 200


@ETapp.route('/earnings', methods=['POST'], strict_slashes=False)
@jwt_required()
def create_earning():
    """ Creates an Earning object """
    current_user = get_current_user()
    if not current_user or not current_user.is_authenticated:
        abort(401)

    if request.is_json:
        try:
            data = request.get_json()
        except BadRequest:
            return jsonify(message='Error parsing JSON data'), 400

        for key in ['name', 'date_occurred', 'amount']:
            if key not in data:
                return jsonify(message=f'{key} missing'), 400

        name = data.get('name').strip()
        description = data.get('description')
        try:
            amount = int(data.get('amount'))
        except (ValueError, TypeError):
            return jsonify(message='Amount must be an integer'), 400

        try:
            date_occurred = datetime.strptime(data.get('date_occurred'), date_format)
        except (ValueError, TypeError) as e:
            return jsonify(message="Invalid date format. Please use 'YYYY-mm-dd'"), 400

        user_earning = Earning(name=name,
                               date_occurred=date_occurred,
                               amount=amount,
                               description=description,
                               user_id=current_user.id)
        user_earning.save()
        return jsonify(message='success', data=user_earning.to_dict()), 201
    return jsonify(message='Not a valid JSON'), 400


@ETapp.route('/earnings/<earning_id>', methods=['DELETE'],
             strict_slashes=False)
@jwt_required()
def delete_earnings(earning_id):
    """ Deletes an earning object """
    current_user = get_current_user()
    if not current_user or not current_user.is_authenticated:
        abort(401)

    obj = db.query(Earning).filter_by(id = earning_id, user_id = current_user.id).first()
    if obj:
        db.delete(obj)
        return jsonify(message='success'), 200

    abort(404)


@ETapp.route('/earnings/<earning_id>', methods=['PUT'],
             strict_slashes=False)
@jwt_required()
def update_earning(earning_id):
    """ Update an earning object """
    current_user = get_current_user()
    if not current_user or not current_user.is_authenticated:
        abort(401)

    if request.is_json:
        try:
            data = request.get_json()
        except BadRequest:
            return jsonify(message='Error parsing JSON data'), 400

        earning = db.query(Earning).filter_by(id = earning_id, user_id = current_user.id).first()
        if not earning:
            abort(404)

        if 'date_occurred' in data:
            date_occurred = data['date_occurred']
            try:
                data['date_occurred'] = datetime.strptime(date_occurred, date_format)
            except (ValueError, TypeError) as e:
                return jsonify(message="Invalid date format. Please use 'YYYY-mm-dd'"), 400

        for key, value in data.items():
            if key in ['name', 'date_occurred', 'amount', 'description']:
                setattr(earning, key, value)

        earning.save()
        return jsonify(message='updated successfully', data=earning.to_dict()), 200

    return jsonify(message='Not a valid JSON'), 400
