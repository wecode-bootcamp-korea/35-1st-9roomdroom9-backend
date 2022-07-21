import json

from django.http  import JsonResponse
from django.views import View

from .models import Product

class ProductDetailView(View):
    def get(self, request, product_id):
        product = Product.objects.get(id=product_id)

        image_list = []
        images = product.productimage_set.all()
        for image in images:
            image_list.append({'img_url' : image.url})

        option_list = []
        options = product.options.all()
        for option in options:
            option_list.append(option.name)
        

        result = {
            'id'      : product.id,
            'name'    : product.name,
            'price'   : product.price,
            'is_green': product.is_green,
            'is_best' : product.is_best,
            'img_urls': image_list,
            'options' : option_list
        }

        return JsonResponse({'result': result}, status=200)