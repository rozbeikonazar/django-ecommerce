from django.shortcuts import render

from .models import Order

# Create your views here.


def cart(request):
    if request.user.is_authenticated:
        user_profile = request.user.profile
        order, created = Order.objects.get_or_create(user_profile=user_profile)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, }

    return render(request, 'cart/cart.html', context={'items': items, 'order': order})

def checkout(request):
    if request.user.is_authenticated:
        user_profile = request.user.profile
        order, created = Order.objects.get_or_create(user_profile=user_profile)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, }
    return render(request, 'cart/checkout.html', context={'items': items, 'order': order})
