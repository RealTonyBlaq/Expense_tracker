#!/usr/bin/env python3
""" The Earning route """

from api.v1 import ETapp
from datetime import datetime
from flask import abort, request, jsonify
from flask_login import login_required, current_user
from models.earning import Earning
from utilities import db


date_format = "%Y-%m-%d"


@login_required
@ETapp.route('/earnings', strict_slashes=False)
@ETapp.route('/earnings/<earning_id>', strict_slashes=False)
def get_earnings(earning_id=None):
    """ Returns an object containing a list of Earning objects """
    if not current_user.is_authenticated:
        return jsonify({'message': 'user not logged in'}), 401

    if earning_id:
        earning = db.query(Earning).filter_by(id = earning_id, user_id = current_user.id).first()
        if earning is not None:
            return jsonify({'message': 'success', 'data': earning.to_dict()}), 200
        abort(404)

    all_earnings = db.all(Earning).values()
    my_earnings = []
    for earning in all_earnings:
        if earning.user_id == current_user.id:
            my_earnings.append(earning.to_dict())

    return jsonify({'message': 'success', 'data': my_earnings}), 200


@login_required
@ETapp.route('/earnings', methods=['POST'], strict_slashes=False)
def create_earning():
    """ Creates an Earning object """
    if not current_user.is_authenticated:
        return jsonify({'message': 'user not logged in'}), 401

    if request.is_json:
        data = request.get_json()
        for key in ['name', 'date_occurred', 'amount']:
            if key not in data:
                return jsonify({'message': f'{key} missing'}), 400

        name = data.get('name')
        amount = int(data.get('amount'))
        description = data.get('description')
        date_occurred = datetime.strptime(data.get('date_occurred'), date_format)

        user_earning = Earning(name=name,
                               date_occurred=date_occurred,
                               amount=amount,
                               description=description,
                               user_id=current_user.id)
        user_earning.save()
        return jsonify({'message': 'success', 'data': user_earning.to_dict()})
    return jsonify({'message': 'Not a valid JSON'}), 400


@ETapp.route('/earnings/<earning_id>')
