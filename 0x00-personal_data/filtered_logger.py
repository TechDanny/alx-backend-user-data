#!/usr/bin/env python3
"""
Regex-ing
"""


import re
from typing import List
import logging


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """returns the log message obfuscated"""
    pattern = (
        fr'({re.escape(separator)}(?:{"|".join(map(re.escape, fields))})='
        r')[^;]+'
    )
    return re.sub(pattern, fr'\1{redaction}', message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
         filter values in incoming log records using filter_datum
        """
        message = super(RedactingFormatter, self).format(record)
        x = filter_datum(self.fields, self.REDACTION, message, self.SEPARATOR)

        return x
