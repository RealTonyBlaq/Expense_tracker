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
    if request.is_json:
        if earning_id:
            earning = db.query(Earning).filter_by(id = earning_id).first()
            if earning is not None:
                return jsonify({'message': earning.to_dict()}), 200
            abort(404)

        fo
    return jsonify({'message': 'Not a valid JSON'}), 400
