from django.urls import path
from .views import cart, checkout, process_order, success_order, update_item

app_name = "cart"


urlpatterns = [
    
    path("browse/", cart, name="cart"),
    path('checkout/', checkout, name="checkout" ),
    path('update_item/', update_item, name='update_item'),
    path('checkout/process', process_order, name='process'),
    path('checkout/success/<int:order_id>/<int:shipping_address_id>/', success_order, name='success')
]
