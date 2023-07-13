from rest_framework import serializers

from products.models import Product, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'quantity', 'slug', 'category' ]



class LowQuantityProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = Product
        fields = ['id', 'name', 'quantity',  'category']

class BestSellerProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    total_sold = serializers.SerializerMethodField()
    class Meta:
        model = Product 
        fields = ['id', 'name', 'category', 'total_sold']

    def get_total_sold(self, obj):
        return obj.total_sold