#!/usr/bin/env python3
import re
import logging
from typing import List

def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """
    Returns the log message obfuscated.
    """
    for field in fields:
        message = re.sub(f"{field}=.*?{separator}", f"{field}={redaction}{separator}", message)
    return message

class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initialize the formatter with fields to redact.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record with redacted fields.
        """
        original_message = super(RedactingFormatter, self).format(record)
        redacted_message = filter_datum(self.fields, self.REDACTION, original_message, self.SEPARATOR)
        return redacted_message

