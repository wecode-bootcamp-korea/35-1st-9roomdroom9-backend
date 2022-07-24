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

            if Cart.objects.filter(user_id = user_id, product_option= product_option).exists():
                cart = Cart.objects.filter(user_id=user_id)
                quantity += cart[0].quantity
                cart.update(quantity=quantity)
                return JsonResponse({'message' : 'CHANGE_CART'}, status=201)

            Cart.objects.create(
                quantity = quantity,
                user_id = user_id,
                product_option_id = product_option,
            )

            return JsonResponse({'message': 'SUCCESS'}, status=200)

        except KeyError as error:
            return JsonResponse({'message': f'{error}'.strip("'")}, status=400)


    @login_required
    def get(self, request):
        try:
            user_id = request.user.id
            carts = Cart.objects.filter(user_id=user_id)
            
            result = [cart for cart in carts:
                a = cart.product_option.product.productimage_set.all()
                b = [image.url for image in a]

                result.append({
                    "cart_id" : cart.id,
                    "quantity" : cart.quantity,
                    "product_name"  : cart.product_option.product.name,
                    "product_image" : b,
                    "product_price" : cart.product_option.product.price,
                    })]

            return JsonResponse({'result': result }, status=200)

        except KeyError as error:
            return JsonResponse({'message': f'{error}'}, status=400)

