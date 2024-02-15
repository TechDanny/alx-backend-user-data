#!/usr/bin/env python3
"""
Auth class
"""


from flask import request
from typing import List, TypeVar
import fnmatch
from os import getenv


User = TypeVar('User')


class Auth:
    """Auth class.
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ returns False - path and excluded_paths will be used later,
        now, you don’t need to take care of them.
        """
        if path is None:
            return True

        if excluded_paths is None or not excluded_paths:
            return True

        for x in excluded_paths:
            if fnmatch.fnmatch(path, x):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """ returns None - request will be the Flask request object
        """
        if request is not None:
            return request.headers.get('Authorization', None)
        return None

    def current_user(self, request=None) -> User:
        """ returns None - request will be the Flask request object
        """
        return None

    def session_cookie(self, request=None):
        """
        returns a cookie value from a request:
        """
        if request is not None:
            return request.cookies.get(getenv('SESSION_NAME',
                                              '_my_session_id'))

        return None
