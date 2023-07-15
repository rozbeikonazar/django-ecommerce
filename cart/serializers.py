from rest_framework import serializers

from cart.models import Cart, CartItem, Order, OrderItem, ShippingAddress


class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = ['name', 'email', 'address', 'country', 'city', 'zipcode' ]

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['product', 'quantity']

class CartSerializer(serializers.ModelSerializer):
    cartitem_set = CartItemSerializer(many=True, read_only=True)
    class Meta:
        model = Cart
        fields = ['id', 'user_profile', 'cartitem_set', 'calculate_cart_total', 'get_cart_items']

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_id = serializers.IntegerField(source='product.id', read_only=True)
    class Meta:
        model = OrderItem
        fields = ['product_id', 'product_name', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    orderitem_set = OrderItemSerializer(many=True, read_only=True)
    shippingaddress_set = ShippingAddressSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'user_profile', 'date_ordered', 'order_status', 'orderitem_set', 'shippingaddress_set']