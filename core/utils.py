import re, jwt, bcrypt

from functools   import wraps
from django.conf import settings
from django.http import JsonResponse

from users.models    import User
from products.models import ProductOption


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
        raise ValueError("INVALID_MOBILE")

def checkEmailExist(value):
    if User.objects.filter(email = value).exists():
        raise ValueError("EXIST_EMAIL")

def checkMobileExist(value):
    if User.objects.filter(mobile_number = value).exists():
         raise ValueError("EXIST_MOBILE_NUMBER")

def hash(value):
    hashed = bcrypt.hashpw(value.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    return hashed

def checkPassword(incomePw, recordedPw):
     encoded_password = incomePw.encode('utf-8')
     user_password    = recordedPw.encode('utf-8')
     if not bcrypt.checkpw(encoded_password, user_password):
         raise ValueError("INVALID_USER")

def createToken(value):
    token = jwt.encode({'id': value}, settings.SECRET_KEY, settings.ALGORITHM)
    return token

def accessCkeck(func):
    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get('Authorization', None)
            payload      = jwt.decode(access_token, settings.SECRET_KEY, settings.ALGORITHM)
            user         = User.objects.get(id = payload['id'])
            request.user = user

        except jwt.exceptions.DecodeError:
            return JsonResponse({'message' : 'INVALID TOKEN'}, status = 400)

        except User.DoesNotExist:
            return JsonResponse({'message' : 'INVALID USER'}, status = 400)
        return func(self, request, *args, **kwargs)

    return wrapper

def checkQuantity(quantity,value):
    if quantity > ProductOption.objects.get(id=value).stock:
        raise ValueError

def get_product_list(products):
    product_list =  [{
        'id'      : product.id,
        'name'    : product.name,
        'price'   : product.price,
        'is_green': product.is_green,
        'is_best' : product.is_best,
        'images'  : [{
            'id' : image.id,
            'url': image.url
            } for image in product.productimage_set.all()]
    } for product in products]
    
    return product_list