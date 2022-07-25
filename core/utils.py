import re, jwt, bcrypt

from functools   import wraps
from django.conf import settings
from django.http import JsonResponse

from users.models import User

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









