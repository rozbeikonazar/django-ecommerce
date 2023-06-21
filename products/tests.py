from django.db import IntegrityError
from django.test import RequestFactory, TestCase
from django.db import transaction
from django.urls import reverse
from products.models import Product, Category
from products.views import search_products, show_product, show_products

class ProductAppModelsTest(TestCase):
    def setUp(self):
        """
        Set up the necessary objects for the test cases.
        """
        self.category = Category.objects.create(name="Test Category")

    def test_category_creation(self):
        """
        Test the creation of a category.
        """
        with transaction.atomic():
            # Valid creation
            created_category = Category.objects.get(name="Test Category")
            self.assertEqual(created_category, self.category)
            
            with self.assertRaises(IntegrityError):
                # Attempt to create a duplicate category, should raise IntegrityError
                Category.objects.create(name="Test Category")

    def test_category_update(self):
        """
        Test updating the name of a category.
        """
        self.category.name = "Test Category 1"
        self.category.save()
        self.assertEqual("Test Category 1", self.category.name)

    def test_product_creation(self):
        """
        Test the creation of a product.
        """
        
        product = Product.objects.create(name="Test Product", description="Test desc", price=1, category=self.category)
        created_product = Product.objects.get(name="Test Product")
        self.assertEqual(created_product, product)
        # Attempt to create product with same slug/name
        with self.assertRaises(IntegrityError):
            Product.objects.create(name="Test product", description="Test desc", price=1, category=self.category)

    def test_product_update(self):
        """
        Test updating the details of a product.
        """
        product = Product.objects.create(name="Test Product", description="Test desc", price=1, category=self.category)
        product.name = "Updated product"
        product.description = "Updated desc"
        product.price = 2
        product.save()
        updated_product = Product.objects.get(name="Updated product")
        self.assertEqual("Updated product", updated_product.name)
    
    def test_product_delete(self):
        """
        Test deleting a product.
        """
        product = Product.objects.create(name="Test Product", description="Test desc", price=1, category=self.category)
        initial_count = Product.objects.count()
        product.delete()
        updated_count = Product.objects.count()
        self.assertEqual(updated_count, initial_count - 1)
        # Not existing product
        with self.assertRaises(Product.DoesNotExist):
            Product.objects.get(pk=product.id)

    def test_category_delete(self):
        """
        Test deleting a category.
        """
        initial_count = Category.objects.count()
        self.category.delete()
        updated_count = Category.objects.count()
        self.assertEqual(updated_count, initial_count - 1)
        # Not existing category
        with self.assertRaises(Category.DoesNotExist):
            Category.objects.get(pk=self.category.id)


class ProductViewsTest(TestCase):
    def setUp(self):
        """
        Set up the necessary objects for the test cases.
        """
        self.factory = RequestFactory()
        self.category = Category.objects.create(name="Test Category")
        self.product = Product.objects.create(name="Test Product", description = "Test desc", price=1, category=self.category)
        
    def test_show_products(self):
        """
        Test for displaying all products.
        """
        url = reverse("products:product_list")
        request = self.factory.get(url)
        response = show_products(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Product")
    
    def test_show_product(self):
        """
        Test for displaying product.
        """
        url = reverse("products:product_details", args=[self.product.slug])
        request = self.factory.get(url)
        response = show_product(request, self.product.slug)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Product")

    def test_search_products(self):
        """
        Test for searching products.
        """
        url = reverse("products:search_products")
        request = self.factory.post(url, {"searched": "Test Product"})
        response = search_products(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Product")
        #not existing product
        request = self.factory.post(url, {"searched": "not existing"})
        response = search_products(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No products found")