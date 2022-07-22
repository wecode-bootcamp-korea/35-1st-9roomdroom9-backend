import re

def checkRegex(REGEX, value):
    if not re.match(REGEX, value):
        raise ValueError