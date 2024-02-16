#!/usr/bin/env python3
"""
sessions in Database
"""


from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from sqlalchemy.orm.exc import NoResultFound


class SessionDBAuth(SessionExpAuth):
    """
    inherits from SessionExpAuth:
    """

    def create_session(self, user_id=None):
        """
        creates and stores new instance of UserSession and returns the
        Session ID
        """
        session_id = super().create_session(user_id)
        if session_id:
            new_session = UserSession(user_id=user_id, session_id=session_id)
            new_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        returns the User ID by requesting UserSession in the database based on
        session_id
        """
        if session_id is None:
            return None

        try:
            user_session = UserSession.search({'session_id': session_id}).one()
            return user_session.user_id
        except NoResultFound:
            return None

    def destroy_session(self, request=None):
        """
        destroys the UserSession based on the Session ID from the request
        cookie
        """
        session_id = self.session_cookie(request)
        if session_id:
            user_session = UserSession.search({'session_id': session_id}
                                              ).first()
            if user_session:
                user_session.remove()
                return True
        return False
