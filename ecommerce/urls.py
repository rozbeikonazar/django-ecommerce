from django.contrib import admin
from django.urls import include, path
from products import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [   path('', views.show_products),
                  path('admin/', admin.site.urls),
                  path('products/', include('products.urls', namespace='products')),
                  path('accounts/', include('accounts.urls', namespace='accounts')),
                  path('cart/', include('cart.urls', namespace='carts')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
