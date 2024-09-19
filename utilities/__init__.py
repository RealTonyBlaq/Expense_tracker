#!/usr/bin/python3
""" Initialization package """

from utilities.database import Database
from utilities.cache import Cache


db = Database()
db.reload()

cache = Cache()
