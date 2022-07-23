import json

from django.views import View
from products.models import *
from orders.models import Cart
from products.models import ProductOption
from django.http  import JsonResponse

class CartView(View):
    def post(self, request):
        try:
            user_id = request.user.id
            product_option_id = request.product_option_id
            data = json.loads(request.body)
            quantity = data['quantity']

            if Cart.objects.filter(pk = product_option_id).exists():
                cart = Cart.objects.get(pk=product_option_id)
                cart.quantity += quantity
                cart.save()
                
                return JsonResponse({'message' : 'CREATE_CART'}, status=201)

            Cart.objects.create(
                quantity = quantity,
                user_id = user_id,
                product_option_id = product_option_id,
            )

            return JsonResponse({'message': 'sucess'}, status=200)

        except KeyError as error:
            return JsonResponse({'message': f'{error}'}, status=400)

    # def get(self, request):
    #     try:
    #         user = request.user
    #         print(cart)
    #         result = []
    #         for cart in carts:
    #             result.append({
    #                 "cart_id" : cart.id,
    #                 "product"  : cart.product.name,
    #                 "product_image_1" : cart.product.name,
    #                 "price" : cart.product.price,
    #                 "quantity" : cart.quantity,
    #                 "product_id" : cart.product.id
    #                 })

    #         return JsonResponse({'result': result }, status=200)

    #     except KeyError as error:
    #         return JsonResponse({'message': f'{error}'}, status=400)

