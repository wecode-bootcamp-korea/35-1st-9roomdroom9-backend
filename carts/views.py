import json

from django.views import View
from django.http  import JsonResponse
from django.db.models   import Prefetch

from core.utils      import accessCkeck, checkQuantity
from orders.models   import Cart
from products.models import ProductImage

class CartView(View):
    @accessCkeck
    def post(self, request):
        try:
            data           = json.loads(request.body)
            user_id        = request.user.id
            quantity       = data['quantity']
            product_option = data['product_option']

            checkQuantity(quantity,product_option)
                
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

    @accessCkeck
    def get(self, request):
        try:
            user_id = request.user.id
            
            carts = (
                Cart.objects
                .select_related(
                    'product_option',
                    'product_option__product',
                    'product_option__option',
                    )
                .prefetch_related(
                    Prefetch(
                        'product_option__product__productimage_set',
                        queryset=(ProductImage.objects.all())
                    )
                )
                .filter(
                    user_id=user_id
                    )
                .order_by(
                    '-updated_at'
                    )
            )
            
            result  = [{
                "cart_id"             : cart.id,
                "quantity"            : cart.quantity,
                "product_id"          : cart.product_option.product.id,
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
    def delete(self, request):
        try:
            user_id  = request.user.id
            cart_ids = request.GET.getlist('cart_id', None)
            
            carts = Cart.objects.filter(user_id=user_id, id__in=cart_ids)          
            carts.delete()

            return JsonResponse({'message' : 'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

        except Cart.DoesNotExist:
            return JsonResponse({'message': 'Cart.DoesNotExist'}, status=400)

        except ValueError:
            return JsonResponse({'message': 'VALUE_ERROR'}, status=400)

        
