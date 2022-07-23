from itertools import product
import json

from django.views import View
from django.http  import JsonResponse

from core.utils import login_required
from products.models import *
from orders.models import Cart
from products.models import ProductOption


class CartView(View):
    @login_required
    def post(self, request):
        try:
            data = json.loads(request.body)
            user_id = request.user.id
            quantity = data['quantity']
            product_option = data['product_option']

            if Cart.objects.filter(user_id = user_id).exists():
                cart = Cart.objects.filter(user_id=user_id)
                quantity += cart[0].quantity
                cart.update(quantity=quantity)
                
                return JsonResponse({'message' : 'CREATE_CART'}, status=201)

            Cart.objects.create(
                quantity = quantity,
                user_id = user_id,
                product_option_id = product_option,
            )

            return JsonResponse({'message': 'sucess'}, status=200)

        except KeyError as error:
            return JsonResponse({'message': f'{error}'}, status=400)


    @login_required
    def get(self, request):
        try:
            user = request.user
            carts = cart.objects.filter(user=user)
            result = []
            for cart in carts:
                result.append({
                    "cart_id" : cart.id,
                    "product"  : cart.product.name,
                    "product_image_1" : cart.product.name,
                    "price" : cart.product.price,
                    "quantity" : cart.quantity,
                    "product_id" : cart.product.id
                    })

            return JsonResponse({'result': result }, status=200)

        except KeyError as error:
            return JsonResponse({'message': f'{error}'}, status=400)

