#!/usr/bin/env python3
"""
Regex-ing
"""


import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """returns the log message obfuscated"""
    pattern = (
        fr'({re.escape(separator)}{"|".join(map(re.escape, fields))}=)'
        r'[^;]+'
    )
    return re.sub(pattern, fr'\1{redaction}', message)
