#!/usr/bin/env python3
"""Module for handling personal data with privacy measures."""

import re
from typing import List
import logging
import os
import mysql.connector


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """
    Filter sensitive data in the log message by
    replacing specified fields with a redaction string.

    Args:
        fields (List[str]): List of field names to be redacted.
        redaction (str): String to replace the sensitive information.
        message (str): The original log message to be filtered.
        separator (str): Character used to separate fields in the log message.

    Returns:
        str: The filtered log message with sensitive information redacted.
    """
    for field in fields:
        regex = f"{field}=[^{separator}]*"
        message = re.sub(regex, f"{field}={redaction}", message)
    return message


class RedactingFormatter(logging.Formatter):
    """Custom formatter to redact sensitive information in log messages."""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initialize the formatter with fields to redact.

        Args:
            fields (List[str]): List of field names to be
                                redacted in log messages.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record, redacting sensitive information.

        Args:
            record (logging.LogRecord): The log record to be formatted.

        Returns:
            str: The formatted log message with sensitive information redacted.
        """
        original_format = super().format(record)
        return filter_datum(
            self.fields, self.REDACTION, original_format, self.SEPARATOR
        )


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def get_logger() -> logging.Logger:
    """
    Creates and configures a logger for handling user data
    securely.

    Returns:
        logging.Logger: Configured logger object with redacting formatter.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Establish a connection to the MySQL database with personal data.

    Returns:
       mysql.connector.connection.MySQLConnection: A connection object
                                                   to the MySQL database.
    """
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME")

    return mysql.connector.connect(
        user=username, password=password, host=host, database=db_name
    )


def main() -> None:
    """
    Main function to retrieve and display filtered user data from the database.
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    log = get_logger()
    for row in cursor:
        data = []
        for desc, value in zip(cursor.description, row):
            pair = f"{desc[0]}={str(value)}"
            data.append(pair)
        row_str = "; ".join(data)
        log.info(row_str)
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
