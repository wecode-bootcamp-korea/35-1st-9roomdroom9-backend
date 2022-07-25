import json

from django.http  import JsonResponse
from django.views import View

from .models    import User
from core.utils import *

class LoginView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            email    = data['email']
            password = data['password']
            user     = User.objects.get(email=email)

            checkPassword(password, user.password)
            return JsonResponse({'message': 'SUCCESS', 'access_token': createToken(user.id)}, status=201)
            
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

        except ValueError:
            return JsonResponse({'message': 'INVALID_USER'}, status=401)

        except User.DoesNotExist:
            return JsonResponse({'message': 'User_DoseNotExist'}, status=404)