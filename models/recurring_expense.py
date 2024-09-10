#!/usr/bin/env python3
""" The Recurring Expense Model """

from models.base import BaseModel, Base
from models.user import User
from sqlalchemy import Column, String, DECIMAL, ForeignKey, DATE
from sqlalchemy.orm import relationship
