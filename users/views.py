import json
import re

import bcrypt
import jwt
from django.http  import JsonResponse
from django.views import View

from .models import User
from django.conf import settings

class SignUpView(View):
    def post(self, request):
        try:
            data          = json.loads(request.body)
            name          = data['name']
            password      = data['password']
            birthday      = data['birthday']   
            mobile_number = data['mobile_number']
            email         = data['email']

            if not re.match('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
                return JsonResponse({'message': 'Email format is not valid'}, status=400)

            if not re.match('^(?=.*[A-Za-z])(?=.*\d)(?=.*[?!@#$%*&])[A-Za-z\d?!@#$%*&]{8,}$', password):
                return JsonResponse({'message': 'Password format is not valid'}, status=400)
            
            if not re.match('^(19[0-9][0-9]|20\d{2})-(0[0-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])$', birthday):
                return JsonResponse({'message':'Date format must be in YYYY-MM-DD'}, status=400)

            if not re.match('^\d{3}-\d{3,4}-\d{4}$', mobile_number): 
                return JsonResponse({'message':'Phone format must be in 01X-XXXX-XXXX'}, status=400)

            if User.objects.filter(email=data.get('email')).exists() and data.get('email') != None:
                return JsonResponse({'MESSAGE': 'ALREADY_EXISTS_EMAIL'}, status = 400)
            
            if User.objects.filter(mobile_number=data.get('mobile_number')).exists() and data.get('mobile_number') != None:
                return JsonResponse({'MESSAGE': 'ALREADY_EXISTS_MOBILE_NUMBER'}, status = 400)

            hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

            User.objects.create(
                name          = name,
                email         = email,
                password      = hashed_password,
                mobile_number = mobile_number,
                birthday      = birthday,
            )
            return JsonResponse({'message': 'SUCCESS'}, status=201)

        except KeyError as e:
            return JsonResponse({'message': f"(KeyError:{e})"}, status=400)


class LoginView(View):
    def post(self, request):
        try:
            data             = json.loads(request.body)
            email            = data['email']
            password         = data['password']
            user             = User.objects.get(email=email)
            user_password    = user.password
            encoded_password = password.encode('utf-8')

            if not bcrypt.checkpw(encoded_password, user_password.encode('utf-8')):
                return JsonResponse({"message": "INVALID_USER"}, status=401)

            token = jwt.encode({'id': user.id}, settings.SECRET_KEY, settings.ALGORITHM)

            return JsonResponse({'message': 'SUCCESS', 'access_token': token})

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

        except User.DoesNotExist:
            return JsonResponse({"message": "INVALID_USER"}, status=401)