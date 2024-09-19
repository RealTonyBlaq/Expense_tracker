#!/usr/bin/env python3
""" The Cache Model """

import redis
from typing import Optional


class Cache:
    """ Defines a Cache class that stores and retrieves items from storage """

    def __init__(self) -> None:
        """ Initializes the Cache class with a Redis instance """
        self.client = redis.Redis()

    def get(self, key: str) -> Optional[str]:
        """ Retrieves value using a key """
        value = self.client.get(key)

        return value.decode('utf-8') if value else None

    def set(self, key: str, value: str, expires_after: float) -> None:
        """ Set/store a value using a key and an expiry time"""
        self.client.setex(key, expires_after, value)

    def delete(self, key: str) -> None:
        """ Deletes a key-value pair """
        self.client.delete(key)
