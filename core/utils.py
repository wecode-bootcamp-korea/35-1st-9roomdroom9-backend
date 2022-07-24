import re, bcrypt

from django.core.exceptions import ObjectDoesNotExist

from users.models import User

def vaildNameRegex(value):
    REGEX_NAME     = '^[가-힣]{2,5}$'
    if not re.match(REGEX_NAME, value):
        raise ValueError("INVALID_NAME")

def validPasswordRegex(value):
    REGEX_PASSWORD = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[?!@#$%*&])[A-Za-z\d?!@#$%*&]{8,}$'
    if not re.match(REGEX_PASSWORD, value):
        raise ValueError("INVALID_PASSWORD")

def validEmailRegex(value):
    REGEX_EMAIL    = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(REGEX_EMAIL, value):
        raise ValueError("INVALID_EMAIL")

def validBirthdayRegex(value):
    REGEX_BIRTHDAY = '^(19[0-9][0-9]|20\d{2})-(0[0-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])$'
    if not re.match(REGEX_BIRTHDAY, value):
        raise ValueError("INVALID_BIRTHDAY")

def validMobileRegex(value):
    REGEX_MOBILE   = '^\d{3}-\d{3,4}-\d{4}$'
    if not re.match(REGEX_MOBILE, value):
        raise ObjectDoesNotExist("EXIST_EMAIL")
def checkEmailExist(value):
    if User.objects.filter(email = value).exists():
        raise ValueError("EXIST_EMAIL")

def checkMobileExist(value):
    if User.objects.filter(mobile_number = value).exists():
         raise ObjectDoesNotExist("EXIST_MOBILE_NUMBER")

def hash(value):
    hashed = bcrypt.hashpw(value.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    return hashed