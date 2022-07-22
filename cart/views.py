from itertools import product
import json
from statistics import quantiles

from django.views import View
from products.models import *
from orders.models import Cart

from django.http  import JsonResponse

class CartCreateView(View):
    def post(self, request):
        try:

            data = json.loads(request.body)
            product = [product for product in ProductOption.objects.all()]
            
            print(ProductOption)

           
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)