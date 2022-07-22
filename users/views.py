import json, bcrypt

from django.http  import JsonResponse
from django.views import View


from .models import User
from core.utils import checkRegex

class SignUpView(View):
    def post(self, request):
        try:
            data           = json.loads(request.body)
            name           = data['name']
            email          = data['email']
            password       = data['password']
            mobile_number  = data['mobile_number']
            birthday       = data.get('birthday')

            REGEX_PASSWORD = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[?!@#$%*&])[A-Za-z\d?!@#$%*&]{8,}$'
            REGEX_EMAIL    = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            REGEX_BIRTHDAY = '^(19[0-9][0-9]|20\d{2})-(0[0-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])$'
            REGEX_MOBILE   = '^\d{3}-\d{3,4}-\d{4}$'

            checkRegex(REGEX_EMAIL, email)
            checkRegex(REGEX_PASSWORD, password)
            checkRegex(REGEX_MOBILE, mobile_number)

            if User.objects.filter(email=email).exists():
                return JsonResponse({'MESSAGE': 'ALREADY_EXISTS_EMAIL'}, status = 400)
                
            if User.objects.filter(mobile_number=mobile_number).exists():
                return JsonResponse({'MESSAGE': 'ALREADY_EXISTS_MOBILE_NUMBER'}, status = 400)

            if birthday: 
                checkRegex(REGEX_BIRTHDAY, birthday)

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
            return JsonResponse({'message': f"(KEY_ERROR:{e})"}, status=400)
        
        except ValueError:
            return JsonResponse({"message": 'Format is not valid'}, status=400)