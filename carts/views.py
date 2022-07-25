import json

from django.views import View
from django.http  import JsonResponse

from core.utils      import accessCkeck
from orders.models   import Cart
from products.models import ProductOption
from products.models import *

class CartView(View):
    @accessCkeck
    def get(self, request):
        try:
            user_id = request.user.id
            carts   = Cart.objects.filter(user_id=user_id)
            result  = [{
                "cart_id"       : cart.id,
                "quantity"      : cart.quantity,
                "product_name"  : cart.product_option.product.name,
                "product_image" : [image.url for image in cart.product_option.product.productimage_set.all()],
                "product_price" : cart.product_option.product.price,
                } for cart in carts]
            return JsonResponse({'result': result}, status=200)

        except KeyError:
            return JsonResponse({'message': 'Key_Error'}, status=400)