import json
import re

import bcrypt
from django.http  import JsonResponse
from django.views import View

from .models import User


class SignUpView(View):
    def post(self, request):
        try:
            data          = json.loads(request.body)
            name          = data['name']
            email         = data['email']
            password      = data['password']
            birthday      = data['birthday']   
            mobile_number = data['mobile_number']

            if not re.match('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
                return JsonResponse({'message': 'Email format is not valid'}, status=400)

            if not re.match('^(?=.*[A-Za-z])(?=.*\d)(?=.*[?!@#$%*&])[A-Za-z\d?!@#$%*&]{8,}$', password):
                return JsonResponse({'message': 'Password format is not valid'}, status=400)
            
            if not re.match('^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$', birthday):
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
                birthday      = birthday
            )
            return JsonResponse({'message': 'SUCCESS'}, status=201)

        except KeyError as e:
            return JsonResponse({'message': f"(KeyError:{e})"}, status=400)
