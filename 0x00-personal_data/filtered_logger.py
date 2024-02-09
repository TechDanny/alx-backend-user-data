#!/usr/bin/env python3
"""
Regex-ing
"""


import re
from typing import List
import logging
import os
import mysql.connector


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """returns the log message obfuscated"""
    for f in fields:
        pattern = r'({0}=)[^{1}]*({1})'.format(f, separator)
        message = re.sub(pattern, r'\1{}\2'.format(redaction), message)
    return message


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


def get_logger() -> logging.Logger:
    """
    returns a logging.Logger object
    """
    logger = logging.getLogger('./user_data')
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(RedactingFormatter(fields=PII_FIELDS))
    logger.setLevel(logging.INFO)
    logger.propagate = False
    logger.addHandler(streamHandler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    returns a connector to the database
    """
    connector = mysql.connector.connect(
        host=os.getenv('PERSONAL_DATA_DB_HOST', "localhost"),
        database=os.getenv('PERSONAL_DATA_DB_NAME'),
        user=os.getenv('PERSONAL_DATA_DB_USERNAME', "root"),
        password=os.getenv('PERSONAL_DATA_DB_PASSWORD', "")
    )
    return connector


def main():
    """
    it obtains a database connection using get_db and retrieve all
    rows in the users table and display each row under a filtered
    format like this:
    """
    connection = get_db()
    logger = get_logger()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    for x in rows:
        message = (
            "name={}; email={}; phone={}; ssn={}; "
            "password={}; ip={}; last_login={}; user_agent={};"
        ).format(
            x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7])
        logger.info(message)
    cursor.close()
    connection.close()


if __name__ == "__main__":
    main()
