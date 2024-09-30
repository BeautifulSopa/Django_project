from django.test import TestCase
from .models import Product

class ProductModelTest(TestCase):
    def setUp(self):
        Product.objects.create(name="Sample Product", price=10.00)
    
    def test_product_name(self):
        product = Product.objects.get(name="Sample Product")
        self.assertEqual(product.price, 10.00)
