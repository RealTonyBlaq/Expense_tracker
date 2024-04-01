#!/usr/bin/python3
""" Initialization package """

from models.engine.database import Database


storage = Database()
storage.reload()
