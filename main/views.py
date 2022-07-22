from django.http  import JsonResponse
from django.views import View

from products.models import Product

class MainPageView(View):
    def get(self, request):
        def get_list(products):
            product_list =  [{
                'id'      : product.id,
                'name'    : product.name,
                'price'   : product.price,
                'is_green': product.is_green,
                'is_best' : product.is_best,
                'images'  : [{
                    'id' : image.id,
                    'url': image.url
                    } for image in product.productimage_set.all()]
            } for product in products]
            return product_list

        new_products   = Product.objects.all().order_by('-created_at')[:8]
        best_products  = Product.objects.filter(is_best = True).order_by('-created_at')[:8] 
        green_products = Product.objects.filter(is_green = True).order_by('-created_at')[:8]

        return JsonResponse({
            'new_products'  : get_list(new_products),
            'best_products' : get_list(best_products),
            'green_products': get_list(green_products)}, status=200)