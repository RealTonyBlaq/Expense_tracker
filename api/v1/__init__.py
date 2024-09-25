#!/usr/bin/python3
""" The Blueprint """

from flask import Blueprint


ETapp = Blueprint('ETapp', __name__, url_prefix='/api/v1')


from api.v1.routes.auth import *
from api.v1.routes.earnings import *
