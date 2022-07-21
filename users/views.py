import json
import re

import bcrypt
from django.http  import JsonResponse
from django.views import View

from .models import User


class SignUpView(View):
    def post(self, request):
        try:
            data           = json.loads(request.body)
            name           = data['name']
            email          = data['email']
            password       = data['password']
            # birthday      = data['birthday']
            birthday       = data.get('birthday')
            mobile_number  = data['mobile_number']

            REGEX_PASSWORD = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[?!@#$%*&])[A-Za-z\d?!@#$%*&]{8,}$'
            # REGEX_EMAIL    = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            # REGEX_BIRTHDAY = '^(19[0-9][0-9]|20\d{2})-(0[0-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])$'
            # REGEX_MOBILE   = '^\d{3}-\d{3,4}-\d{4}$'

            checkRegexPassword(REGEX_PASSWORD,password)
    
            # print('-----birthday type:', bool(birthday))
            # print('-----birthday :', birthday)

            # if not re.match(REGEX_EMAIL, email):
            #     return JsonResponse({'message': 'Email format is not valid'}, status=400)

            # if not re.match(REGEX_PASSWORD, password):
            #     return JsonResponse({'message': 'Password format is not valid'}, status=400)
            
            # if not re.match(REGEX_BIRTHDAY, birthday):
            #     return JsonResponse({'message':'Date format must be in YYYY-MM-DD'}, status=400)

            # if not re.match(REGEX_MOBILE, mobile_number): 
            #     return JsonResponse({'message':'Phone format must be in 01X-XXXX-XXXX'}, status=400)
            
            if User.objects.filter(email=email).exists():
                return JsonResponse({'MESSAGE': 'ALREADY_EXISTS_EMAIL'}, status = 400)
            
            if User.objects.filter(mobile_number=mobile_number).exists():
                return JsonResponse({'MESSAGE': 'ALREADY_EXISTS_MOBILE_NUMBER'}, status = 400)

            hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

            User.objects.create(
                name          = name,
                email         = email,
                password      = hashed_password,
                mobile_number = mobile_number,
                birthday      = birthday
            )
            return JsonResponse({'message': 'SUCCESS'}, status=201)

        except KeyError as e:
            return JsonResponse({'message': f"(KeyError:{e})"}, status=400)
        
        except ValueError as e:
            return JsonResponse({'message': "valueError"}, status=400)
            
            
def checkRegexPassword(REGEX,key):
    re.compile(REGEX) != key
    raise ValueError(JsonResponse({'message': 'Password format is not valid'}, status=400))
