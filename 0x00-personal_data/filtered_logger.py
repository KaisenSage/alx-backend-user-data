#!/usr/bin/env python3
"""
This module contains a function to filter and obfuscate PII fields.
"""
import re
from typing import List

def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """
    Replaces occurrences of certain field values with a redaction string.
    """
    for field in fields:
        message = re.sub(f"{field}=.*?{separator}", f"{field}={redaction}{separator}", message)
    return message

