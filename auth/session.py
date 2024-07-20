#!/usr/bin/env python3
""" Session AUthentication Module """

from bcrypt import checkpw, gensalt, hashpw
from datetime import datetime, timedelta
from models.engine.database import Database
import random
from typing import List
from auth.user_session import UserSession
from models.user import User


def _hashed_password(password: str) -> str:
    """ Generates a hashed password using bcrypt """
    password = password.encode('utf-8')
    salt = gensalt()
    return hashpw(password, salt)

def _token() -> int:
    """ Returns a 6-digit token """
    return random.randint(10000, 99999)


class Auth:
    """ Defining the Session class """
    __session_duration = 60

    def __init__(self) -> None:
        """ Initializing the attributes """
        self._DB = Database()

    def session_cookie(self, request=None) -> str:
        """ Returns the session id from the request """
        if request:
            cookie = request.cookies.get('session_id')
            return cookie
        return None

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Checks if authentication is required for the assessed path """
        if path and excluded_paths:
            for excluded_path in excluded_paths:
                if excluded_path.endswith('*'):
                    if path.startswith(excluded_path[:-1]):
                        return False
            
            if path[-1] != '/':
                path += '/'
            if path in excluded_paths:
                return False
            return True
        return False

    def create_session(self, email: str) -> str:
        """ Creates a session_id for a User and returns it """
        if email:
            user = self._DB.get_user(email)
            if user:
                new_session = UserSession(user_id=user.id)
                new_session.save()
                return new_session.id
        return None

    def find_user_by_session_id(self, session_id: str) -> User:
        """ Retrieves a User object using session_id """
        if session_id and type(session_id) is str:
            obj = self._DB.find(UserSession, session_id)
            if obj:
                user = self._DB.find(User, obj.user_id)
                if self.__session_duration <= 0:
                    return user
                current_time = datetime.now()
                duration = timedelta(seconds=self.__session_duration)
                if current_time > obj.created_at + duration:
                    return None
                return user
                
        return None

    def delete_usersession(self, session_id: str) -> None:
        """ Deletes the UserSession obj that matches a user_id """
        if session_id and type(session_id) is str:
            session = self._DB.find(UserSession, session_id)
            if session:
                self._DB.delete(session)
        return None

    def validate(self, email: str, password: str) -> bool:
        """ Validates a User account """
        if email and password:
            try:
                user = self._DB.get_user(email)
                return checkpw(password.encode('utf-8'), user.password)
            except ValueError:
                pass
        return False

    def create_user(self, kwargs: dict) -> str:
        """ Creates a User and returns the object id """
        if kwargs:
            # Check if dictionary contains keys-value needed for User creation
            deets = ['first_name', 'last_name', 'email', 'password']
            for deet in deets:
                if deet not in kwargs.keys():
                    raise ValueError(f'{deet} missing')

            # check if User email already exists
            try:
                self._DB.get_user(kwargs['email'])
                raise ValueError('User -> {} exists'.format(kwargs['email']))
            except ValueError:
                # If ValueError is raised, it means email is valid
                for key, value in kwargs.items(): 
                    if key == 'password':
                        kwargs[key] = _hashed_password(value)
                user = User(**kwargs)
                user.save()
                return user.id

    def create_reset_token(self, user_id: str) -> str:
        """ Sets a token for a User in a UserSession obj """
        if user_id:
            try:
                self._DB.find(User, user_id)
                reset_token = _token()
                session = UserSession(user_id=user_id, reset_token=reset_token)
                session.save()
                return reset_token
            except (TypeError, ValueError):
                pass
        return None   

    def update_password(self, email: str, password: str, reset_token: int) -> None:
        """ Updates a User password """
        if email and password and reset_token:
            try:
                user = self._DB.get_user(email)
            except ValueError:
                return None

            try:
                sess_obj = self._DB.fetch_session_obj_by(reset_token=reset_token)
            except Exception:
                return None

            if sess_obj.user_id == user.id:
                self._DB.update_password(user.id, _hashed_password(password))
                self._DB.delete(sess_obj)
        return None

    def current_user(self, request) -> User:
        """ Returns the User object that matches a session id """
        if request:
            cookie = self.session_cookie(request)
            user = self.find_user_by_session_id(cookie)
            return user
        return None
