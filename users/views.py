import json, bcrypt, jwt

from django.http  import JsonResponse
from django.views import View
from django.conf  import settings

from .models import User
from core import utils

class SignUpView(View):
    def post(self, request):
        try:
            data           = json.loads(request.body)
            name           = data['name']
            email          = data['email']
            password       = data['password']
            mobile_number  = data['mobile_number']
            birthday       = data.get('birthday')

            utils.vaildNameRegex(name)
            utils.validEmailRegex(email)
            utils.validPasswordRegex(password)
            utils.validMobileRegex(mobile_number)
            utils.checkEmailExist(email)
            utils.checkMobileExist(mobile_number)

            if birthday: 
                utils.validBirthdayRegex(birthday)

            hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

            User.objects.create(
                name          = name,
                email         = email,
                password      = hashed_password,
                mobile_number = mobile_number,
                birthday      = birthday,
            )
            return JsonResponse({'message': 'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

        except ValueError as e :
            return JsonResponse({"message": f'{e}'}, status=400)


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
                return JsonResponse({'message': 'INVALID_USER'}, status=401)

            token = jwt.encode({'id': user.id}, settings.SECRET_KEY, settings.ALGORITHM)

            return JsonResponse({'message': 'SUCCESS', 'access_token': token})

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

        except User.DoesNotExist:
            return JsonResponse({'message': 'INVALID_USER'}, status=401)
