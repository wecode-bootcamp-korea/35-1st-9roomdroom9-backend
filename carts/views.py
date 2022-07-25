import json

from django.views import View
from django.http  import JsonResponse

from core.utils      import login_required
from orders.models   import Cart
from products.models import ProductOption
from products.models import *

class CartView(View):
    @login_required
    def post(self, request):
        try:
            data           = json.loads(request.body)
            user_id        = request.user.id
            quantity       = data['quantity']
            product_option = data['product_option']

            if Cart.objects.filter(user_id = user_id, product_option = product_option).exists():
                cart      = Cart.objects.filter(user_id=user_id)
                quantity += cart[0].quantity
                cart.update(quantity=quantity)
                return JsonResponse({'message' : 'CHANGE_CART'}, status=201)

            Cart.objects.create(
                quantity          = quantity,
                user_id           = user_id,
                product_option_id = product_option,
            )

            return JsonResponse({'message': 'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)