#!/usr/bin/env python3
""" The Category Route """

from api.v1 import ETapp
from flask_jwt_extended import jwt_required, get_current_user
from models.category import Category
from utilities import db


@ETapp.route('/categories', strict_slashes=False)
@ETapp.route('/categories/<category_id>', strict_slashes=False)
def get_categories(category_id):
    """ Returns a list of categories with the associating Expenses """
    if category_id:
        category = db.query(Category).filter_by(id = )
