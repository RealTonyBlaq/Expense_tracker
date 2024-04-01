#!/usr/bin/python3
"""This module defines a base class for all models in expense tracker"""

from datetime import datetime
from flask import Flask, render_template
import uuid


class Expense:
     """A base class for all expense tracker models"""

    def __init__(self, name="", category="", amount=0.00, id=0):
       self.name = name
        self.category = category
        self.amount = amount
        id = str(uuid.uuid4())

        
    app = Flask (__name__)

    @app.route('/')
    @app.route('/home')
    def home():
        return render_template(home.html)
