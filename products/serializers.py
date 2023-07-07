from rest_framework import serializers

from products.models import Product, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'quantity', 'slug', 'name', 'category' ]




