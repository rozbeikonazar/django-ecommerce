from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import show_products, show_product, search_products

app_name = 'products'

urlpatterns = [
    path('', show_products, name='product_list'),
    path('details/<slug:slug>', show_product, name='product_details'),
    path('category/<str:category_name>/', show_products, name='category'),
    path('search_products', search_products, name='search_products'), 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)