#!/usr/bin/python3
""" The Category route """

from api import ETapp
from flask import abort, make_response, jsonify
from models.category import Category
from models import storage
