from django.db import models
from accounts.models import Profile
from products.models import Product
from django.db.models import Sum, F

class Cart(models.Model):
    user_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    
    @property 
    def calculate_cart_total(self):
        cart_items = self.cartitem_set.filter(quantity__gt=0, product__quantity__gt=0)
        total = cart_items.aggregate(cart_total=Sum(F('product__price') * F('quantity')))['cart_total']
        return total or 0
    
    @property
    def get_cart_items(self):
        cart_items = self.cartitem_set.filter(quantity__gt=0, product__quantity__gt=0)
        total = cart_items.aggregate(total_items=Sum('quantity'))['total_items']
        return total or 0
    
    @property
    def delete_invalid_cart_items(self):
        cart_items = self.cartitem_set.filter(quantity__lte=0) | self.cartitem_set.filter(product__quantity__lte=0)
        cart_items.delete()

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField(default=0, blank=True, null=True)
    
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total or 0




class Order(models.Model):
    ORDER_STATUSES = (
        ('processing', 'Processing'),
        ('shippinng', 'Shipping'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        )
    user_profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(choices=ORDER_STATUSES, max_length=50, default=False)
    transaction_id = models.CharField(max_length=200, null=True)


    def __str__(self):
        return f"ID: {self.id}"
    
    @property
    def calculate_order_total(self):
        order_items = self.orderitem_set.filter(quantity__gt=0, product__quantity__gt=0)
        total = order_items.aggregate(order_total=Sum(F('product__price')* F('quantity')))['order_total']
        return total or 0
    
    
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return f"Order id: {self.order.id}, Product name: {self.product.name}"
    

class ShippingAddress(models.Model):
    user_profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=True)
    country = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)


    def __str__(self):
        return f"Order_id: {self.order.id}, Address: {self.address}"
    
