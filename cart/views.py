import json

from django.views import View

class CartCreateView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            a =
            productname = data['productname']
            productimage_url = data['productname']
            print(product.id)
           
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)