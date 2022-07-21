import json

from django.http  import JsonResponse
from django.views import View

from .models import Product, Category

class ProductListView(View):
    def get(self, request, cat_id=1000):
        result = []
        # 전체리스트
        if cat_id == 1000:
            products = Product.objects.all()

        #카테고리별
        else:
            products = Product.objects.filter(category_id=cat_id)
            if not Category.objects.filter(id=cat_id).exists():
                return JsonResponse({'message':'CATEGORY_DOES_NOT_EXIST'}, status=400)

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
                'total'   : products.count()
            }
            result.append(product_information)

        return JsonResponse({'result': result}, status=200)