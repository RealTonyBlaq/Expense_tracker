#!/usr/bin/python3
""" The Blueprint """

from flask import Blueprint


ETapp = Blueprint('ETapp', __name__, url_prefix='/api')


from api.routes.users import *
