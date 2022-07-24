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

        except KeyError as error:
            return JsonResponse({'message': f'{error}'.strip("'")}, status=400)

    @login_required
    def get(self, request):
        try:
            user_id = request.user.id
            carts   = Cart.objects.filter(user_id=user_id)
            result  = [{
                "cart_id" : cart.id,
                "quantity" : cart.quantity,
                "product_name"  : cart.product_option.product.name,
                "product_image" : {image.id: image.url for image in cart.product_option.product.productimage_set.all()},
                "product_price" : cart.product_option.product.price,
                } for cart in carts]
            return JsonResponse({'result': result}, status=200)

        except KeyError as error:
            return JsonResponse({'message': f'{error}'.strip("'")}, status=400)
        
    @login_required
    def delete(self, request):
        try:
            user_id  = request.user.id
            carts_id = request.GET.getlist('cart_id', None)
            for cart_id in carts_id:
                carts = Cart.objects.filter(id = cart_id, user_id = user_id)
                carts.delete()

            return JsonResponse({'result': 'SUCCESS'}, status=200)
        
        except KeyError as error:
            return JsonResponse({'message': f'{error}'.strip("'")}, status=400)

    @login_required
    def patch(self, request):
        try:
            data     = json.loads(request.body)
            user_id  = request.user.id
            carts_id = request.GET.getlist('cart_id', None)
            print(carts_id)
            quantity = data['quantity']
            for cart_id in carts_id:
                carts = Cart.objects.filter(id = cart_id, user_id = user_id)
                carts.update(quantity = quantity)
            return JsonResponse({'result': 'SUCCESS'}, status=200)

        except KeyError as error:
            return JsonResponse({'message': f'{error}'.strip("'")}, status=400)
