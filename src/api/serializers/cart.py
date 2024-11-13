from rest_framework import serializers

from api.serializers.product import ProductReadSerializer
from cart.models import Cart, CartItem
from products.models import Product


class CartItemReadSerializer(serializers.ModelSerializer):
    product = ProductReadSerializer()

    class Meta:
        model = CartItem
        fields = ("id", "product", "quantity")
        read_only_fields = fields


class CartItemWriteSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    quantity = serializers.IntegerField(min_value=1)

    class Meta:
        model = CartItem
        fields = ("product", "quantity")


class CartReadSerializer(serializers.ModelSerializer):
    items = CartItemReadSerializer(source="cart_items", many=True)
    total_quantity = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ("id", "user", "items", "total_quantity", "total_price")
        read_only_fields = fields

    def get_total_quantity(self, obj: Cart):
        return sum(item.quantity for item in obj.cart_items.all())

    def get_total_price(self, obj: Cart):
        return sum(item.quantity * item.product.price for item in obj.cart_items.all())
