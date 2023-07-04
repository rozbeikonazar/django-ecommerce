import json
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from cart.forms import DeliveryInformationForm
from products.models import Product
from products.views import change_products_quantity
from .models import Order, OrderItem, PurchaseItem, ShippingAddress
from django.contrib.auth.decorators import login_required


def get_order_items(request):
    if request.user.is_authenticated:
        user_profile = request.user.profile
        order, _ = Order.objects.get_or_create(user_profile=user_profile)
        items = order.orderitem_set.all().order_by('id')
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
    return items, order

@login_required
def cart(request):
    title = "Cart"
    items, order = get_order_items(request)
    return render(request, 'cart/cart.html', context={'items': items, 'order': order, 'title': title})

@login_required
def checkout(request):
    items, order = get_order_items(request)
    return render(request, 'cart/checkout.html', context={'items': items, 'order': order})

@login_required
def update_item(request):
    data = json.loads(request.body)
    product_id = data.get('productId')
    action = data.get('action')

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


def process_order(request):
    items, order = get_order_items(request)

    if request.method == 'POST':
        form = DeliveryInformationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            address = form.cleaned_data['address']
            country = form.cleaned_data['country']
            city = form.cleaned_data['city']  
            zipcode = form.cleaned_data['zipcode']
            
            shipping_address = ShippingAddress.objects.create(
                user_profile=request.user.profile,
                order=order,
                name = name,
                email = email,
                address=address,
                country=country,
                city=city, 
                zipcode=zipcode
            )

            order.order_status = 'processing'
            change_products_quantity(items)
            order.orderitem_set.all().delete()
            order.save()
            
            
            
            return redirect('cart:success', order_id=order.id, shipping_address_id = shipping_address.id)

        else:
            return render(request, 'cart/checkout.html', {'form': form, 'items': items, 'order': order, 'error': 'Invalid form data'})

    else:
        form = DeliveryInformationForm()
        return render(request, 'checkout.html', {'form': form, 'items': items, 'order': order})
    
@login_required
def success_order(request, order_id, shipping_address_id):
    order = get_object_or_404(Order, id=order_id, user_profile=request.user.profile)
    shipping_address = get_object_or_404(ShippingAddress, id=shipping_address_id, user_profile=request.user.profile)
    order_items = PurchaseItem.objects.filter(order_id=order_id)
    context = {'order': order, 'shipping_address': shipping_address, "order_items": order_items}
    return render(request, "cart/success_order.html", context)