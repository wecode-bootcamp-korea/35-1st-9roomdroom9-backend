import json
from os import access

from django.views import View
from django.http  import JsonResponse

from core.utils      import accessCkeck
from orders.models   import Cart

class CartView(View):
    @accessCkeck
    def post(self, request):
        try:
            data           = json.loads(request.body)
            user_id        = request.user.id
            quantity       = data['quantity']
            product_option = data['product_option']
            
            own_cart = Cart.objects.select_related('product_option').filter(user_id=user_id,product_option= product_option)

            if own_cart.exists():
                if quantity not in list(range(1,10000)) or own_cart[0].product_option.stock - quantity < 0:
                    raise ValueError
                quantity += own_cart[0].quantity
                own_cart.update(quantity=quantity)
                return JsonResponse({'message' : 'CHANGE_CART'}, status=201)

            Cart.objects.create(
                quantity          = quantity,
                user_id           = user_id,
                product_option_id = product_option,
            )
            return JsonResponse({'message': 'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        
        except Cart.DoesNotExist:
            return JsonResponse({'message': 'Cart.DoesNotExist'}, status=400)
        
        except ValueError:
            return JsonResponse({'message': 'VALUE_ERROR'}, status=400)
