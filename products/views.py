import math

from django.http  import JsonResponse
from django.views import View

from .models    import Product, Category
from decorators import query_debugger

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

class ProductListView(View):
    @query_debugger
    def get(self, request, category_id):
        try:
            offset = int(request.GET.get('offset', 0))
            limit  = int(request.GET.get('limit', 6))

            category = Category.objects.get(id=category_id)
            products = Product.objects.all()

            if category_id != 1000:
                products = Product.objects.filter(category_id=category_id)

            total_products = products.count()

            category_data = {
                'id'            : category.id,
                'name'          : category.name,
                'description'   : category.description,
                'total_products': total_products
                }
            
            sort_by = {
                None        : 'id',
                'NEW'       : '-created_at',
                'HIGH_PRICE': '-price',
                'LOW_PRICE' : 'price'
            }

            products = products.prefetch_related('productimage_set').order_by(sort_by[request.GET.get('sorting', None)])[offset:offset+limit]

            # if offset: 
            #     offset = int(offset)
            # else: 
            #     offset = 0
            # if limit: 
            #     limit = int(limit)
            # else: 
            #     limit = total_products - offset
            
            # products = products[ offset : offset + limit ]

            # page_data = {
            #     'current_page' : math.floor( (offset + limit) / limit ),
            #     'next'    : None if offset + limit > total_products else f'/products/{category.id}?limit={limit}&offset={offset+limit}',
            #     'previous': None if offset - limit < 0              else f'/products/{category.id}?limit={limit}&offset={offset-limit}'
            # }

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
                'category_data': category_data,
                # 'page_data'    : page_data,
                'products_data': products_data}, status=200)

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

            products = Product.objects.all()


            for product in products:
                print(product.id, product.name)

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
                    'option_id'           : option.id,
                    'name'                : option.name,
                    'product_option_id'   : product.productoption_set.get(option_id=option.id).id,
                    'product_option_stock': product.productoption_set.get(option_id=option.id).stock
                    } for option in options]
            }

            return JsonResponse({'result': result}, status=200)
            
        except Product.DoesNotExist:
            return JsonResponse({'message': 'PRODUCT_DOES_NOT_EXIST'}, status=400)