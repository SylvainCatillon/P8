from django.test import TestCase
from django.urls import reverse

from unittest.mock import Mock
from unittest import skip

import pdb

from .models import Product
from .utils.fill_db import FillDB

nutrients = ['fat','saturated-fat','sugars','salt']
MOCK_PRODUCTS = [
        {"nutrition_grade_fr": "a",
        "categories_tags": ["en:test"],
        "product_name": "test1",
        "url": "https//test.com",
        "image_front_small_url": "https//test.com",
        "nutrient_levels": {e: "low" for e in nutrients},
        'nutriments': {e+'_100g': '2' for e in nutrients}},
        {"nutrition_grade_fr": "b",
        "categories_tags": ["en:test"],
        "product_name": "test2",
        "url": "https//test2.com",
        "image_front_small_url": "https//test2.com"},
    ]

class TestFillDB(TestCase):

    def tearDown(self):
        for product in Product.objects.all():
                product.delete()

    def test_insert_products(self):
        self.assertEqual(Product.objects.count(), 0)
        fill_db = FillDB()
        fill_db.dl_products = Mock(return_value=MOCK_PRODUCTS)
        result = fill_db.insert_products()
        fill_db.dl_products.assert_called_once()
        self.assertQuerysetEqual(
            list(Product.objects.all()),
            ['<Product: Test1>','<Product: Test2>'])

    @skip("very long test using API call")
    def test_insert_products_no_mock(self):
        self.assertEqual(Product.objects.count(), 0)
        fill_db = FillDB()
        result = fill_db.insert_products()
        self.assertGreater(Product.objects.count(), 200)

class TestSearchProduct(TestCase):
    

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        fill_db = FillDB()
        fill_db.dl_products = Mock(return_value=MOCK_PRODUCTS)
        fill_db.insert_products()
    
    @classmethod
    def tearDownClass(cls):
        for product in Product.objects.all():
                product.delete()
        super().tearDownClass()

    # test find a product by name
    def test_find_a_product(self):
        # count how many product the search should find
        query = "test"
        test_products = 0
        for product in MOCK_PRODUCTS:
            if query in product["product_name"]:
                test_products += 1
        # test if the search find the right amout of products
        response = self.client.get(
            f"{reverse('substitut:search')}?query={query}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["products"]), test_products)

    # test if the founded substitut has a better nutriscore and is in the same category
    def test_find_a_substitut(self):
        product = Product.objects.order_by('-nutriscore')[0]
        response = self.client.get(
            f"{reverse('substitut:find')}?product_id={product.id}")
        self.assertLess(
            response.context['products'][0].nutriscore, product.nutriscore)

class TestProductPage(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        fill_db = FillDB()
        fill_db.dl_products = Mock(return_value=MOCK_PRODUCTS[:1])
        fill_db.insert_products()

    @classmethod
    def tearDownClass(cls):
        for product in Product.objects.all():
                product.delete()
        super().tearDownClass()

    # test product page contains the required informations    
    def test_product_page(self):
        product = Product.objects.get(
            name=MOCK_PRODUCTS[0]["product_name"].title())
        product_id = product.id
        response = self.client.get(
            f"{reverse('substitut:detail')}?product_id={product_id}")
        self.assertContains(response, product.name)
        self.assertContains(response, product.nutriscore)
        self.assertContains(response, product.link)
        for level in product.nutrient_levels:
            self.assertContains(response, level)
