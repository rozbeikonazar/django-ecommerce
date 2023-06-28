from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator
from django.core.cache import cache


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, db_index=True)
    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"
    

    def save(self, *args, **kwargs):
        cache.delete(settings.CATEGORIES_CACHE)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Category: {self.name}"


class Product(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    description = models.TextField(db_index=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(1)])
    image = models.ImageField(upload_to='products_images/', null=True)
    slug = models.SlugField(max_length=200,unique=True, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        cache.delete(settings.PRODUCTS_CACHE)
        cache.delete(f"products_{self.category.name}")
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "product"
        verbose_name_plural = "products"
    
    def __str__(self):
        return f'Product: {self.name}'
