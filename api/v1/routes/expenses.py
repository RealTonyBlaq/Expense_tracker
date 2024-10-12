#!/usr/bin/env python3
""" The Expense Route """

from api.v1 import ETapp
from models.category import Category
from models.expense import Expense
from flask_jwt_extended import get_current_user, jwt_required
from werkzeug.exceptions import BadRequest, BadRequestKeyError


@ETapp.route('/expenses', sstrict_slashes=False)
@ETapp.route('/expenses/<expense_id>', strict_slashes=False)
@jwt_required()
def get_expenses(expense_id):
    """ Retrieves a JSON representation """
