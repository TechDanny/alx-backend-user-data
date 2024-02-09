#!/usr/bin/env python3
"""
 Encrypting passwords
"""


import bcrypt


def hash_password(password: str) -> bytes:
    """
    This function returns a salted, hashed password, which is a byte string.
    """
    random_salt = bcrypt.gensalt()
    hash_pswd = bcrypt.hashpw(password.encode('utf-8'), random_salt)

    return hash_pswd
