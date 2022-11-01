from django.test import TestCase, Client

from .models import Product, Category, ProductImage, Option, ProductOption

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
                id         = 1,
                url        = 'url1',
                product_id = 1
            ),
            ProductImage(
                id         = 2,
                url        = 'url2',
                product_id = 1
            )
        ])
        Option.objects.bulk_create([
            Option(
                id   = 1,
                name = 'option1'
            ),
            Option(
                id   = 2,
                name = 'option2'
            ),
            Option(
                id   = 3,
                name = 'option3'
            )
        ])
        ProductOption.objects.bulk_create([
            ProductOption(
                id         = 1,
                stock      = 100,
                product_id = 1,
                option_id  = 1
            ),
            ProductOption(
                id         = 2,
                stock      = 50,
                product_id = 1,
                option_id  = 2
            )
        ])

    def tearDown(self):
        Category.objects.all().delete() # 얘만 삭제하면 cascade되지만 혹시나해서 다삭제,,,,
        Product.objects.all().delete()
        ProductImage.objects.all().delete()

    def test_success_productdetailview_get(self):
        client   = Client()
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
                'options' : [
                    {
                        'option_id'           : 1,
                        'name'                : 'option1',
                        'product_option_id'   : 1,
                        'product_option_stock': 100
                    },
                    {
                        'option_id'           : 2,
                        'name'                : 'option2',
                        'product_option_id'   : 2,
                        'product_option_stock': 50
                    }
                ],
            }
        })

    def test_fail_productdetailview_get_product_not_exist(self):
        client   = Client()
        response = client.get('/products/detail/2')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {
            'message': 'PRODUCT_DOES_NOT_EXIST'
        })
