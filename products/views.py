import json

from django.http  import JsonResponse
from django.views import View

from .models import Product, Category

class ProductListView(View):
    def get(self, request, cat_id=None):
        result = []

        # 전체리스트
        if cat_id == None:
            products = Product.objects.all()

        #카테고리별
        else:   
            products = Product.objects.filter(category_id=cat_id)

            if not Category.objects.filter(id=cat_id).exists():
                return JsonResponse({'message':'CATEGORY_DOES_NOT_EXIST'}, status=400)

        result.append({'total': products.count()})

        for product in products:
            images = product.productimage_set.all()
            product_information = {
                'id'      : product.id,
                'name'    : product.name,
                'price'   : product.price,
                'is_green': product.is_green,
                'is_best' : product.is_best,
                'img_urls': [image.url for image in images]
            }
            result.append(product_information)

        return JsonResponse({'result': result}, status=200)