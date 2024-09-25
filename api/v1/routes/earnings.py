#!/usr/bin/env python3
""" The Earning route """

from api.v1 import ETapp
from datetime import datetime
from flask_login import login_required, current_user
from models.earning import Earning


date_format = "%Y-%m-%d"


@login_required
@ETapp.route('/earnings', strict_slashes=False)
@ETapp.route('/earnings/<id>', strict_slashes=False)
def get_earnings(id=None):
    """ Returns an object containing a list of Earning objects """
    if id:
        
