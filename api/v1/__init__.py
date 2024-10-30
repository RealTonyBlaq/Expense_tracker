#!/usr/bin/python3
""" The Blueprint """

from flask import Blueprint


ETapp = Blueprint('ETapp', __name__, url_prefix='/api/v1')
date_format = "%Y-%m-%d"


from api.v1.routes.auth import *
from api.v1.routes.earnings import *
from api.v1.routes.categories import *
from api.v1.routes.expenses import *
from api.v1.routes.recurring_expenses import *
from api.v1.routes.self import *
