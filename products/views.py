import json

from django.http  import JsonResponse
from django.views import View

from .models import Product

class ProductDetailView(View):
    def get(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)

            images  = product.productimage_set.all()
            options = product.options.all()

            result = {
                'id'      : product.id,
                'name'    : product.name,
                'price'   : product.price,
                'is_green': product.is_green,
                'is_best' : product.is_best,
                'img_urls': [image.url for image in images],
                'options' : [option.name for option in options]
            }
            return JsonResponse({'result': result}, status=200)
        except Product.DoesNotExist:
            return JsonResponse({'message': 'PRODUCT_DOES_NOT_EXIST'}, status=400)