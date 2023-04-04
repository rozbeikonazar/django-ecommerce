import json
from django.shortcuts import render
from django.http import JsonResponse

from products.models import Product
from .models import Order, OrderItem

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


def update_item(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print(f"action: {action}, productId: {productId}")

    user_profile = request.user.profile
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(user_profile=user_profile)
    orderItem , created = OrderItem.objects.get_or_create(order=order, product=product)
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == "remove":
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse("Item was added", safe=False)