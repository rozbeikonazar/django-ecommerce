from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"
    
    def __str__(self):
        return f"Category: {self.name}"

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products_images/', blank=False) 
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    
    class Meta:
        verbose_name = "product"
        verbose_name_plural = "products"
    
    def __str__(self):
        return f'Product: {self.name}'
