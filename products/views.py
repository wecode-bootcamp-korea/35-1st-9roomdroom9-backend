import json

from django.http  import JsonResponse
from django.views import View

from .models import Product

class ProductListView(View):
    def get(self, request):
        result   = []
        products = Product.objects.all()

        for product in products:
            images     = product.productimage_set.all()
            image_list = []

            for image in images:
                image_list.append(image.url)

            product_information = {
                'id'      : product.id,
                'name'    : product.name,
                'price'   : product.price,
                'is_green': product.is_green,
                'is_best' : product.is_best,
                'img_urls': image_list,
                'total' : products.count()
            }
            result.append(product_information)

        return JsonResponse({'result': result}, status=200)