#!/usr/bin/python3
""" The Blueprint """

from flask import Blueprint, jsonify
from flask_jwt_extended import get_current_user
from functools import wraps


ETapp = Blueprint('ETapp', __name__, url_prefix='/api/v1')
date_format = "%Y-%m-%d"


def admin_required(func):
    """ Checks if a user is an admin, else access is denied """
    @wraps(func)
    def wrapper(*args, **kwargs):
        user = get_current_user()
        if user.is_admin is False:
            return jsonify(message="Oops! Access denied"), 403
        return func(*args, **kwargs)

    return wrapper


from api.v1.routes.admin import *
from api.v1.routes.auth import *
from api.v1.routes.earnings import *
from api.v1.routes.categories import *
from api.v1.routes.expenses import *
from api.v1.routes.recurring_expenses import *
from api.v1.routes.self import *
