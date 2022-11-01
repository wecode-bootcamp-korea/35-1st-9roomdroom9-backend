from django.test import TestCase, Client

from .models import Product, Category

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
                'price'   : '1234.56',
                'is_green': False,
                'is_best' : False,
                'images'  : [],
                'options' : [],
            }
        })
