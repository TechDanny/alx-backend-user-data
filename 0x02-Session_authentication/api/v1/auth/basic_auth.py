#!/usr/bin/env python3
"""
Basic auth
"""


from .auth import Auth
import re
import base64
import binascii
from typing import Tuple, TypeVar
from models.user import User


class BasicAuth(Auth):
    """
    inherits from Auth
    """
    User = TypeVar("User")

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
         returns the Base64 part of the Authorization header for a
         Basic Authentication
        """
        if type(authorization_header) == str:
            pattern = r'Basic (?P<token>.+)'
            fieldMatch = re.fullmatch(pattern, authorization_header.strip())
            if fieldMatch is not None:
                return fieldMatch.group('token')
        return None

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """
        returns the decoded value of a Base64 string
        base64_authorization_header
        """
        if type(base64_authorization_header) == str:
            try:
                result = base64.b64decode(
                    base64_authorization_header,
                    validate=True,
                )
                return result.decode('utf-8')
            except (binascii.Error, UnicodeDecodeError):
                return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> Tuple[str, str]:
        """
        returns the user email and password from the Base64 decoded value
        """
        if type(decoded_base64_authorization_header) == str:
            passwd_pattern = r'(?P<user>[^:]+):(?P<password>.+)'
            fieldMatch = re.fullmatch(
                passwd_pattern,
                decoded_base64_authorization_header.strip(),
            )
            if fieldMatch is not None:
                user = fieldMatch.group('user')
                passwd = fieldMatch.group('password')
                return user, passwd
        return None, None

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> User:
        """
        returns the User instance based on his email and password.
        """
        if type(user_email) == str and type(user_pwd) == str:
            try:
                user = User.search({'email': user_email})
            except Exception:
                return None
            if len(user) <= 0:
                return None
            if user[0].is_valid_password(user_pwd):
                return user[0]
        return None

    def current_user(self, request=None) -> User:
        """
        it overloads Auth and retrieves the User instance for a request
        """
        header = self.authorization_header(request)
        b64_token = self.extract_base64_authorization_header(header)
        token = self.decode_base64_authorization_header(b64_token)
        email, passwd = self.extract_user_credentials(token)
        return self.user_object_from_credentials(email, passwd)
