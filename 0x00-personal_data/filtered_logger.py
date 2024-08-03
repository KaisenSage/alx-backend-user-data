#!/usr/bin/env python3
import re
import logging
from typing import List
import os
import mysql.connector
from mysql.connector.connection import MySQLConnection
import bcrypt

# Task 0: Regex-ing
def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """
    Returns the log message obfuscated.
    """
    for field in fields:
        message = re.sub(f"{field}=.*?{separator}", f"{field}={redaction}{separator}", message)
    return message

# Task 1: Log formatter
class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

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

# Task 2: Create logger
PII_FIELDS = ("name", "email", "phone", "ssn", "password")

def get_logger() -> logging.Logger:
    """
    Creates a logger object with specific settings.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger

# Task 3: Connect to secure database
def get_db() -> MySQLConnection:
    """
    Connect to a secure MySQL database.
    """
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    database = os.getenv("PERSONAL_DATA_DB_NAME")
    
    return mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=database
    )

# Task 4: Read and filter data
def main() -> None:
    """
    Obtain a database connection and retrieve all rows in the users table.
    Display each row under a filtered format.
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    for row in cursor:
        message = f"name={row[0]};email={row[1]};phone={row[2]};ssn={row[3]};password={row[4]};ip={row[5]};last_login={row[6]};user_agent={row[7]};"
        logger = get_logger()
        logger.info(message)
    cursor.close()
    db.close()

if __name__ == "__main__":
    main()

# Task 5: Encrypting passwords
def hash_password(password: str) -> bytes:
    """
    Hash a password using bcrypt.
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

# Task 6: Check valid password
def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Check if the provided password matches the hashed password.
    """
    return bcrypt.checkpw(password.encode(), hashed_password)

