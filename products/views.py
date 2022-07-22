from django.http  import JsonResponse
from django.views import View

from .models import Product, Category

class ProductListView(View):
    def get(self, request, category_id=None):
        result = []

        products = Product.objects.all()

        if category_id:
            if not Category.objects.filter(id=category_id).exists():
                return JsonResponse({'message':'CATEGORY_DOES_NOT_EXIST'}, status=400)
            products = Product.objects.filter(category_id=category_id)

        result.append({'total': products.count()})

        for product in products:
            images = product.productimage_set.all()
            product_information = {
                'id'      : product.id,
                'name'    : product.name,
                'price'   : product.price,
                'is_green': product.is_green,
                'is_best' : product.is_best,
                'images'  : [{
                    'id' : image.id,
                    'url': image.url
                    } for image in images]
            }
            result.append(product_information)

        return JsonResponse({'result': result}, status=200)