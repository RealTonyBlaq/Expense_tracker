#!/usr/bin/python3
""" Initialization package """

from utilities.database import Database


db = Database()
db.reload()
