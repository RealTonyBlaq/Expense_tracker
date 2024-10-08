#!/usr/bin/env python3
""" The Category Route """

from api.v1b
from flask_jwt_extended import jwt_required, get_current_user
from models.category import Category
from utilities import db
