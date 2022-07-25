import json

from django.views import View
from django.http  import JsonResponse

from core.utils      import accessCkeck
from orders.models   import Cart
from products.models import ProductOption
from products.models import *

class CartView(View): 
    @accessCkeck
    def delete(self, request):
        try:
            user_id  = request.user.id
            carts_id = request.GET.getlist('cart_id', None)
            for cart_id in carts_id:
                carts = Cart.objects.filter(id = cart_id, user_id = user_id)
                carts.delete()

            return JsonResponse({'result': 'SUCCESS'}, status=200)
        
        except KeyError as error:
            return JsonResponse({'message': "Key_Error"}, status=400)
