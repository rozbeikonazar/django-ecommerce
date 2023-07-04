from django.db import models
from accounts.models import Profile
from products.models import Product



class Order(models.Model):
    ORDER_STATUSES = (
        ('cart', 'Cart'),
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        )
    user_profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(choices=ORDER_STATUSES, max_length=50, default=False)
    transaction_id = models.CharField(max_length=200, null=True)
    
    @property 
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = 0
        for item in orderitems:
            if item.quantity <= 0 or item.product.quantity <= 0:
                item.delete()
            else:
                total += item.get_total
        return total
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = 0
        for item in orderitems:
            if item.quantity <= 0 or item.product.quantity <= 0:
                item.delete()
            else:
                total += 1
        return total

    def __str__(self):
        return f"ID: {self.id}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.order_status == 'processing':
            # Create PurchaseItem instances for each OrderItem and associate them with the order
            order_items = self.orderitem_set.all()
            for order_item in order_items:
                PurchaseItem.objects.create(order=self, product=order_item.product, quantity=order_item.quantity)
    

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, blank=True, null=True)

    @property
    def get_total(self):
        if self.product:
            total = self.product.price * self.quantity
            return total
        return 0

    def __str__(self):
        return f"Product name: {self.product.name}"


class ShippingAddress(models.Model):
    user_profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=True)
    country = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)


    def __str__(self):
        return self.address
    
class PurchaseItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"Order ID: {self.order.id}, Product: {self.product.name}, Quantity: {self.quantity}"