from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import show_products, show_product

app_name = 'products'

urlpatterns = [
    path('', show_products, name='product_list'),
    path('details/<int:id>', show_product, name='product_details'),
    path('category/<str:category_name>/', show_products, name='category'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)