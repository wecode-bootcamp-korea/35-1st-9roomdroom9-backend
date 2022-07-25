from django.http  import JsonResponse
from django.views import View

from .models import Product, Category

class ProductListView(View):
    def get(self, request, category_id=1000):
        try:
            category = Category.objects.get(id=category_id)
            products = Product.objects.all()

            if category_id != 1000:
                products = Product.objects.filter(category_id=category_id)
            
            sort_by = {
                None        : 'id',
                'NEW'       : '-created_at',
                'HIGH_PRICE': '-price',
                'LOW_PRICE' : 'price'
            }
            products = products.order_by(sort_by[request.GET.get('sorting', None)])

            category_data = {
                'id'            : category.id,
                'description'   : category.description,
                'total_products': products.count()
                }

            products_data = [{
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

            return JsonResponse({
                'products_data' : products_data,
                'category_data' : category_data}, status=200)

        except Category.DoesNotExist:
            return JsonResponse({'message':'CATEGORY_DOES_NOT_EXIST'}, status=400)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

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
                'images'  : [{
                    'id' : image.id,
                    'url': image.url
                    } for image in images],
                'options' : [{
                    'id'  : option.id,
                    'name': option.name
                    } for option in options]
            }
            return JsonResponse({'result': result}, status=200)
            
        except Product.DoesNotExist:
            return JsonResponse({'message': 'PRODUCT_DOES_NOT_EXIST'}, status=400)