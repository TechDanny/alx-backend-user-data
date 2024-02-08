#!/usr/bin/env python3
"""
Regex-ing
"""


import re


def filter_datum(fields, redaction, message, separator):
    """returns the log message obfuscated"""
    log_message = re.sub(fr'({re.escape(separator)}{"|".join(map(re.escape, fields))}=)[^;]+', fr'\1{redaction}', message)
    return log_message
