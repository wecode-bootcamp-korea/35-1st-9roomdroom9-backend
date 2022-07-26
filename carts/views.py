import json

from django.views import View
from django.http  import JsonResponse

from core.utils      import accessCkeck
from orders.models   import Cart

class CartView(View):
    @accessCkeck
    def get(self, request):
        try:
            user_id = request.user.id
            carts   = Cart.objects.select_related('product_option').filter(user_id=user_id).order_by('-updated_at')
            result  = [{
                "cart_id"             : cart.id,
                "quantity"            : cart.quantity,
                "product_name"        : cart.product_option.product.name,
                "product_option_id"   : cart.product_option.id,
                "product_option_name" : cart.product_option.option.name,
                "product_image"       : [image.url for image in cart.product_option.product.productimage_set.all()],
                "product_price"       : cart.product_option.product.price,
                "product_stock"       : cart.product_option.stock,
                } for cart in carts]
            return JsonResponse({'result': result}, status=200)
        
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        
        except Cart.DoesNotExist:
            return JsonResponse({'message': 'Cart.DoesNotExist'}, status=400)