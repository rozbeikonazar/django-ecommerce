from django.contrib import admin
from django.urls import include, path
from accounts.rest_views import CustomUserViewSet
from products import views
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers
from products.rest_views import ProductViewSet
from cart.rest_views import CartViewSet

router = routers.DefaultRouter()
router.register(r'products', ProductViewSet, basename='products')
router.register(r'accounts', CustomUserViewSet, basename='accounts')
router.register(r'carts', CartViewSet, basename='carts')


urlpatterns = [   path('', views.show_products),
                  path('admin/', admin.site.urls),
                  path('products/', include('products.urls', namespace='products')),
                  path('accounts/', include('accounts.urls', namespace='accounts')),
                  path('cart/', include('cart.urls', namespace='carts')),
                  path('api/', include(router.urls))
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
