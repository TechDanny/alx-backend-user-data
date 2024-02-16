#!/usr/bin/env python3
"""
Empty session
"""

from flask import jsonify, request, abort
from api.v1.views import app_views
from api.v1.auth.auth import Auth
import uuid
from models.user import User
from os import getenv


class SessionAuth(Auth):
    """
     inherits from Auth
    """
    user_id_by_session_id = {}
    session_name = getenv('SESSION_NAME', '_my_session_id')

    def create_session(self, user_id: str = None) -> str:
        """
        creates a Session ID for a user_id:
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())

        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        returns a User ID based on a Session ID:
        """
        if session_id is None or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> User:
        """
        returns a User instance based on a cookie value:
        """
        session_id = self.session_cookie(request)
        if session_id:
            user_id = self.user_id_for_session_id(session_id)
            if user_id:
                return User.get(user_id)

        return None

    def destroy_session(self, request=None) -> bool:
        """
        deletes the user session / logout:.
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if not session_id:
            return False

        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return False

        del self.user_id_by_session_id[session_id]
        return True
