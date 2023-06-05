import json
from django.shortcuts import render
from django.http import JsonResponse
from products.models import Product
from .models import Order, OrderItem

def get_order_items(request):
    if request.user.is_authenticated:
        user_profile = request.user.profile
        order, _ = Order.objects.get_or_create(user_profile=user_profile)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
    return items, order

def cart(request):
    title = "Cart"
    items, order = get_order_items(request)
    return render(request, 'cart/cart.html', context={'items': items, 'order': order, 'title': title})

def checkout(request):
    items, order = get_order_items(request)
    return render(request, 'cart/checkout.html', context={'items': items, 'order': order})

def update_item(request):
    data = json.loads(request.body)
    product_id = data.get('productId')
    action = data.get('action')
    print(f"action: {action}, productId: {product_id}")

    if request.user.is_authenticated:
        user_profile = request.user.profile
        product = Product.objects.get(id=product_id)
        order, _ = Order.objects.get_or_create(user_profile=user_profile)
        order_item, _ = OrderItem.objects.get_or_create(order=order, product=product)
        if action == 'add':
            order_item.quantity += 1
        elif action == "remove":
            order_item.quantity -= 1
        order_item.save()

        if order_item.quantity <= 0:
            order_item.delete()
        return JsonResponse("Item was added", safe=False)
    else:
        return JsonResponse("User is not authenticated", safe=False)
