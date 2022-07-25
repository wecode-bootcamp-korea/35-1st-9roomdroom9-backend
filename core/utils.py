import re, jwt, bcrypt

from core.utils import *

from users.models import User

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