from rest_framework import viewsets, filters
from products.models import Product
from products.serializers import ProductSerializer, LowQuantityProductSerializer, BestSellerProductSerializer
from django.db.models import Sum


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class LowQuantityProductsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(quantity__lt=5).order_by('quantity')
    serializer_class = LowQuantityProductSerializer


class BestSellerProductsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BestSellerProductSerializer

    def get_queryset(self):
        return Product.objects.annotate(total_sold=Sum('orderitem__quantity')).order_by('-total_sold')