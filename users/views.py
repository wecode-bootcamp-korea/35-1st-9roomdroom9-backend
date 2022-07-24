import json

from django.http            import JsonResponse
from django.views           import View
from django.core.exceptions import ObjectDoesNotExist

from .models    import User
from core.utils import *


class SignUpView(View):
    def post(self, request):
        try:
            data          = json.loads(request.body)
            name          = data['name']
            email         = data['email']
            password      = data['password']
            mobile_number = data['mobile_number']
            birthday      = data.get('birthday')

            vaildNameRegex(name)
            validEmailRegex(email)
            validPasswordRegex(password)
            validMobileRegex(mobile_number)
            checkEmailExist(email)
            checkMobileExist(mobile_number)

            if birthday: 
                validBirthdayRegex(birthday)

            User.objects.create(
                name          = name,
                email         = email,
                password      = hash(password),
                mobile_number = mobile_number,
                birthday      = birthday
            )
            return JsonResponse({'message': 'SUCCESS'}, status=201)

        except KeyError as error:
            return JsonResponse({'message': f'{error}'.strip("'")}, status=400)

        except ValueError as error:
            return JsonResponse({'message': f'{error}'.strip("'")}, status=401)
        
        except ObjectDoesNotExist as error:
            return JsonResponse({'message': f'{error}'.strip("'")}, status=404)


class LoginView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            email    = data['email']
            password = data['password']
            user     = User.objects.get(email=email)

            checkPassword(password, user.password)

            return JsonResponse({'message': 'SUCCESS', 'access_token': createToken(user.id)}, status=201)

        except KeyError as error:
            return JsonResponse({'message': f'{error}'.strip("'")}, status=400)
        
        except ValueError:
            return JsonResponse({'message': 'INVALID_USER'}, status=401)

        except ObjectDoesNotExist as error:
            return JsonResponse({'message': f'{error}'.strip("'")}, status=404)