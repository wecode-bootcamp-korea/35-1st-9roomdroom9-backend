from urllib import response
from django.test import TestCase, Client

from .models import Product, Category, ProductImage

class ProductDetailTest(TestCase):
    def setUp(self):
        Category.objects.create(
            id          = 1,
            name        = 'testcategory',
            description = '테스트를위한카테고리'
        )
        Product.objects.create(
            id          = 1,
            name        = 'testproduct',
            price       = 1234.56,
            is_green    = False,
            is_best     = False,
            category_id = 1
        )
        ProductImage.objects.bulk_create([
            ProductImage(
                id = 1,
                url = 'url1',
                product_id = 1
            ),
            ProductImage(
                id = 2, 
                url = 'url2',
                product_id =1
            )
        ])

    def tearDown(self):
        Category.objects.all().delete()
        Product.objects.all().delete()

    def test_success_productdetailview_get(self):
        client = Client()

        response = client.get('/products/detail/1')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'result' : {
                'id'      : 1,
                'name'    : 'testproduct',
                'price'   : '1234.56', # decimal 타입은 문자열로 인식
                'is_green': False,
                'is_best' : False,
                'images'  : [
                    {
                        'id' : 1,
                        'url': 'url1'
                    },
                    {
                        'id' : 2,
                        'url': 'url2'
                    }
                ],
                'options' : [],
            }
        })
    def test_fail_productdetailview_get_product_not_exist(self):
        client   = Client()
        response = client.get('/products/detail/2')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {
            'message': 'PRODUCT_DOES_NOT_EXIST'
        })
