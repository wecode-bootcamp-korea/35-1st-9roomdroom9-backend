import json

from django.views import View
from django.http  import JsonResponse

from core.utils      import accessCkeck
from orders.models   import Cart
from products.models import ProductOption

class CartView(View):
    @accessCkeck
    def get(self, request):
        try:
            '''
            orm 최적화
            '''
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

    @accessCkeck
    def post(self, request):
        try:
            data           = json.loads(request.body)
            user_id        = request.user.id
            quantity       = data['quantity']
            product_option = data['product_option']
            
            # own_cart = Cart.objects.select_related('product_option').filter(user_id=user_id,product_option= product_option)

            if quantity > ProductOption.objects.get(id=product_option).stock or . . .:
                . . .

            # if own_cart.exists():
            #     if quantity not in list(range(1,10000)) or own_cart[0].product_option.stock - quantity < 0:
            #         raise ValueError
            #     quantity += own_cart[0].quantity
            #     own_cart.update(quantity=quantity)
            #     return JsonResponse({'message' : 'CHANGE_CART'}, status=201)

            cart, is_created = Cart.objects.get_or_create(
                user_id           = user_id,
                product_option_id = product_option,
                defaults          = {
                    'quantity' : quantity,
                }
            )

            if not is_created:
                cart.quantity += quantity
            
            cart.save()

            return JsonResponse({'message': 'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        
        except Cart.DoesNotExist:
            return JsonResponse({'message': 'Cart.DoesNotExist'}, status=400)
        
        except ValueError:
            return JsonResponse({'message': 'VALUE_ERROR'}, status=400)

    # @accessCkeck
    # def patch(self, request):
    #     try:
    #         data     = json.loads(request.body)
    #         user_id  = request.user.id
    #         carts_id = request.GET.getlist('cart_id', None)
    #         print(carts_id)
    #         quantity = data['quantity']
    #         for cart_id in carts_id:
    #             carts = Cart.objects.filter(id = cart_id, user_id = user_id)
    #             carts.update(quantity = quantity)
    #         return JsonResponse({'result': 'SUCCESS'}, status=200)

    #     except KeyError:
    #         return JsonResponse({'message': "KEY_ERROR"}, status=400)

    @accessCkeck
    def delete(self, request):
        try:
            '''
            cart_ids = request.GET.getlist('cart_id', None)
            cart_ids = request.GET.get('cart_id', None)

            http -v DELETE localhost:8000/carts?cart_id=1&cart_id=2&cart_id=3
            http -v DELETE localhost:8000/carts?cart_id=1,2,3

            ['1', '2', '3']
            1,2,3
            '''
            user_id  = request.user.id
            cart_ids = request.GET.getlist('cart_id', None)

            carts = Cart.objects.filter(user_id=user_id, id__in=cart_ids)
            carts.delete()

            # for cart_id in carts_id:
            #     carts = Cart.objects.select_related('product_option').filter(id = cart_id, user_id = user_id)
            #     carts.delete()

            # remain_cart   = Cart.objects.filter(user_id=user_id)
            # result  = [{
            #     "cart_id"             : cart.id,
            #     "quantity"            : cart.quantity,
            #     "product_name"        : cart.product_option.product.name,
            #     "product_option_id"   : cart.product_option.id,
            #     "product_option_name" : cart.product_option.option.name,
            #     "product_image"       : [image.url for image in cart.product_option.product.productimage_set.all()],
            #     "product_price"       : cart.product_option.product.price,
            #     "product_stock"       : cart.product_option.stock,
            #     } for cart in remain_cart]
            # return JsonResponse({'message': 'SUCESSE', 'result': result}, status=200)

            return JsonResponse({'message' : 'DELETE_SUCCESS'}, status=204)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

        except Cart.DoesNotExist:
            return JsonResponse({'message': 'Cart.DoesNotExist'}, status=400)

        except ValueError:
            return JsonResponse({'message': 'VALUE_ERROR'}, status=400)
