import re

def filter_datum(fields, redaction, message, separator):
    """
    Returns the log message obfuscated

    Arguments:
    fields (list): a list of strings representing all fields to obfuscate
    redaction (str): a string representing by what the field will be obfuscated
    message (str): a string representing the log line
    separator (str): a string representing by which character is separating all fields in the log line (message)
    """
    for field in fields:
        message = re.sub(f"{field}=[^{separator}]+", f"{field}={redaction}", message)
    return message

# Example usage
fields = ["password", "date_of_birth"]
messages = [
    "name=egg;email=eggmin@eggsample.com;password=eggcellent;date_of_birth=12/12/1986;", 
    "name=bob;email=bob@dylan.com;password=bobbycool;date_of_birth=03/04/1993;"
]

for message in messages:
    print(filter_datum(fields, 'xxx', message, ';'))

