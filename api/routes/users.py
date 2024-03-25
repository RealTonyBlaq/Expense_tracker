#!/usr/bin/python3
""" Module for API route for the User """

from api import ETapp
from models import storage
from models.user import User


ETapp.route('/users')
