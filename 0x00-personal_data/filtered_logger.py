#!/usr/bin/env python3
"""
Regex-ing
"""


import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """returns the log message obfuscated"""
    log_message = re.sub(fr'({re.escape(separator)}{"|".join(map(re.escape, fields))}=)[^;]+', fr'\1{redaction}', message)
    return log_message
