#!/usr/bin/env python3
""" The Earning route """

from api.v1 import ETapp
from datetime import datetime
from flask import request
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
        if id:
            earning = db.query(Earning).filter_by(id =)
