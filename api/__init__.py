#!/usr/bin/python3
""" The Blueprint """

from flask import Blueprint


ETapp = Blueprint('ETapp', __name__, url_prefix='/api')


from api.routes.categories import *
from api.routes.users import *
from api.routes.expenses import *
from web_flask.app import *
