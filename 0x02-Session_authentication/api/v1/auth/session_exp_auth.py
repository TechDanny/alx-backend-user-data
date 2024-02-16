#!/usr/bin/env python3
"""
Expiration
"""


from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
from os import getenv


class SessionExpAuth(SessionAuth):
    """
     inherits from SessionAuth
    """
    def __init__(self):
        """
        Assign an instance attribute session_duration.
        """
        super().__init__()
        self.session_duration = int(getenv('SESSION_DURATION', 0))

    def create_session(self, user_id=None):
        """
        Return the Session ID create
        """
        session_id = super().create_session(user_id)
        if session_id:
            session_dict = self.user_id_by_session_id.get(session_id, {})
            session_dict.update({
                'user_id': user_id,
                'created_at': datetime.now()
            })
            self.user_id_by_session_id[session_id] = session_dict
            return session_id
        return None

    def user_id_for_session_id(self, session_id=None):
        """
        return user_id from the session dictionary.
        """
        if session_id is None:
            return None

        session_dict = self.user_id_by_session_id.get(session_id)
        if not session_dict:
            return None

        user_id = session_dict.get('user_id')
        created_at = session_dict.get('created_at')

        if self.session_duration <= 0:
            return user_id

        if not created_at:
            return None

        expiration_time = created_at + timedelta(seconds=self.session_duration)
        if expiration_time < datetime.now():
            return None

        return user_id
