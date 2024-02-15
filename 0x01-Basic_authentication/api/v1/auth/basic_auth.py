#!/usr/bin/env python3
"""
Basic auth
"""


from .auth import Auth
import re
import base64
import binascii


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
