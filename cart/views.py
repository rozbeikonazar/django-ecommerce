import json
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from cart.forms import DeliveryInformationForm
from products.models import Product
from products.views import update_products_quantity
from .models import Cart, CartItem, Order, OrderItem, ShippingAddress
from django.contrib.auth.decorators import login_required


def set_order_items(cart_items, order):
    """
    Set order items based on cart items
    """
    for cart_item in cart_items:
        order_item = OrderItem.objects.create(product=cart_item.product, order=order,  quantity=cart_item.quantity)
        order_item.save()


def get_cart_items(request):
    """
    Get the cart items for the give
    """
    if request.user.is_authenticated:
        user_profile = request.user.profile
        cart, _ = Cart.objects.get_or_create(user_profile=user_profile)
        items = cart.cartitem_set.all().order_by('id')
    else:
        items = []
        cart = {'get_cart_total': 0, 'get_cart_items': 0}
    return items, cart

@login_required
def cart(request):
    """
    Render the cart page and display cart items that the user has added
    """
    title = "Cart"
    items, cart = get_cart_items(request)
    return render(request, 'cart/cart.html', context={'items': items, 'cart': cart, 'title': title})

@login_required
def checkout(request):
    """
    Render the checkout page and display cart items that the user has added
    """
    title = "Checkout"
    items, cart = get_cart_items(request)
    if items:
        return render(request, 'cart/checkout.html', context={'items': items, 'cart': cart, 'title': title})
    
    error_message = "Your cart is empty. Please add items to your cart before proceeding to checkout."
    return render(request, 'cart/checkout.html', {'error_message': error_message})

@login_required
def update_item(request):
    """
    Updates the quantity of a cart item
    """
    data = json.loads(request.body)
    product_id = data.get('productId')
    action = data.get('action')

    if request.user.is_authenticated:
        user_profile = request.user.profile
        product = Product.objects.get(id=product_id)
        cart, _ =  Cart.objects.get_or_create(user_profile=user_profile)
        cart_item, _ = CartItem.objects.get_or_create(cart=cart, product=product)
        
        if action == 'add' and cart_item.quantity < product.quantity:
            cart_item.quantity += 1
        elif action == 'remove':
            cart_item.quantity -= 1
        
        cart_item.save()
        
        if cart_item.quantity <= 0 or product.quantity <= 0:
            cart_item.delete()

        

        return JsonResponse("Item was updated", safe=False)
    else:
        return JsonResponse("User is not authenticated", safe=False)



def process_order(request):
    """
    Process the order and complete the checkout process. 
    """
    items, cart = get_cart_items(request)

    if request.method == 'POST':
        form = DeliveryInformationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            address = form.cleaned_data['address']
            country = form.cleaned_data['country']
            city = form.cleaned_data['city']  
            zipcode = form.cleaned_data['zipcode']
            order = Order.objects.create(user_profile=cart.user_profile, order_status='processing')
            
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
            set_order_items(items, order=order)
            update_products_quantity(items)
            cart.delete()
            return redirect('cart:success', order_id=order.id, shipping_address_id = shipping_address.id)

        else:
            return render(request, 'cart/checkout.html', {'form': form, 'items': items, 'cart': cart, 'error': 'Invalid form data'})

    else:
        form = DeliveryInformationForm()
        return render(request, 'checkout.html', {'form': form, 'items': items, 'cart': cart})
    
@login_required
def success_order(request, order_id, shipping_address_id):
    """
    Render the success order page
    """
    title = f"Success order №{order_id}"
    order = get_object_or_404(Order, id=order_id, user_profile=request.user.profile)
    shipping_address = get_object_or_404(ShippingAddress, id=shipping_address_id, user_profile=request.user.profile)
    order_items = OrderItem.objects.filter(order_id=order_id)
    context = {'order': order, 'shipping_address': shipping_address, "order_items": order_items, 'title': title}
    return render(request, "cart/success_order.html", context)