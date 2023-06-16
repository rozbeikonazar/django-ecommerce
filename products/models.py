from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"
    
    def __str__(self):
        return f"Category: {self.name}"

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(1)])
    image = models.ImageField(upload_to='products_images/', null=True)
    slug = models.SlugField(max_length=200,unique=True, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name = "product"
        verbose_name_plural = "products"
    
    def __str__(self):
        return f'Product: {self.name}'
