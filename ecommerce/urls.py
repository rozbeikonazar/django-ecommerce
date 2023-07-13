from django.contrib import admin
from django.urls import include, path
from accounts.rest_views import CustomUserViewSet, ProfileViewSet, TopBuyers
from products import views
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers
from products.rest_views import ProductViewSet, LowQuantityProductsViewSet, BestSellerProductsViewSet
from cart.rest_views import CartViewSet, OrderViewSet

router = routers.DefaultRouter()
router.register(r'products/low-quantity-products', LowQuantityProductsViewSet, basename='low-quantity-products')
router.register(r'products/bestsellers', BestSellerProductsViewSet, basename='bestsellers')
router.register(r'accounts/topbuyer', TopBuyers, basename='topbuyer' )
router.register(r'products', ProductViewSet, basename='products')
router.register(r'accounts', ProfileViewSet, basename='accounts')
router.register(r'carts', CartViewSet, basename='carts')
router.register(r'orders', OrderViewSet, basename='orders')




urlpatterns = [   path('', views.show_products),
                  path('admin/', admin.site.urls),
                  path('products/', include('products.urls', namespace='products')),
                  path('accounts/', include('accounts.urls', namespace='accounts')),
                  path('cart/', include('cart.urls', namespace='carts')),
                  path('api/', include(router.urls))
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
