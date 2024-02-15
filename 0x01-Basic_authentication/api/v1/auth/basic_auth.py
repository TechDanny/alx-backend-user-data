#!/usr/bin/env python3
"""
Basic auth
"""


from .auth import Auth
import re


class BasicAuth(Auth):
    """
    inherits from Auth
    """
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
