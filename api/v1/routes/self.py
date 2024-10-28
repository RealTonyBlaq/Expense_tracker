#!/usr/bin/env python3
""" The current user route """

from api.v1 import ETapp
from datetime import datetime
from flask import abort, jsonify, request
from flask_jwt_extended import jwt_required, get_current_user
from models.user import User
from models.category import Category
from models.earning import Earning
from models.expense import Expense
from models.recurring_expense import RecurringExpense
from models.tag import Tag
from utilities import db
from werkzeug.exceptions import BadRequest


@ETapp.route('/me', methods=['GET', 'PATCH', 'DELETE'], strict_slashes=False)
@jwt_required()
def get_me():
    """
    GET /me - Returns a JSON with the user information
    PATCH /me - Resets a user's password and other data
    
    """
    current_user = get_current_user()
    if not current_user or not current_user.is_authenticated:
        abort(401)

    category = db.query(Category).filter_by(user_id = current_user.id).all()
    