import json, jwt

from django.http  import JsonResponse
from django.views import View
from django.conf  import settings

from .models import User
from core.utils import *


class SignUpView(View):
    def post(self, request):
        try:
            data           = json.loads(request.body)
            name           = data['name']
            email          = data['email']
            password       = data['password']
            mobile_number  = data['mobile_number']
            birthday       = data.get('birthday')

            vaildNameRegex(name)
            validEmailRegex(email)
            validPasswordRegex(password)
            validMobileRegex(mobile_number)
            checkEmailExist(email)
            checkMobileExist(mobile_number)

            if birthday: 
                validBirthdayRegex(birthday)

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
            return JsonResponse({'message': f'{e}'}, status=400)

        except ValueError as e :
            return JsonResponse({"message": f'{e}'}, status=400)


class LoginView(View):
    def post(self, request):
        try:
            data             = json.loads(request.body)
            email            = data['email']
            password         = data['password']
            user             = User.objects.get(email=email)

            checkPassword(password, user.password)

            token = jwt.encode({'id': user.id}, settings.SECRET_KEY, settings.ALGORITHM)

            return JsonResponse({'message': 'SUCCESS', 'access_token': token.decode('utf-8')})

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        
        except ValueError:
            return JsonResponse({'message': 'INVALID_USER'}, status=401)

        except User.DoesNotExist:
            return JsonResponse({'message': 'INVALID_USER'}, status=401)