from decimal import Decimal
from django.db.models import Sum, F, DecimalField
from rest_framework import serializers

from api.constants import MIN_QUANTITY
from api.serializers.product import ProductReadSerializer
from cart.models import Cart, CartItem
from products.models import Product


class CartItemReadSerializer(serializers.ModelSerializer):
    """Serializer for reading CartItem instances"""

    product = ProductReadSerializer()

    class Meta:
        model = CartItem
        fields = ("id", "product", "quantity")
        read_only_fields = fields


class CartItemWriteSerializer(serializers.ModelSerializer):
    """Serializer for writing CartItem instances."""

    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    quantity = serializers.IntegerField(min_value=MIN_QUANTITY)

    class Meta:
        model = CartItem
        fields = ("product", "quantity")


class CartReadSerializer(serializers.ModelSerializer):
    """Serializer for reading Cart instances"""

    items = CartItemReadSerializer(source="cart_items", many=True)
    total_quantity = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ("id", "user", "items", "total_quantity", "total_price")
        read_only_fields = fields

    def get_total_quantity(self, cart: Cart):
        """Calculates the total quantity of all items in the cart."""
        return cart.cart_items.aggregate(total=Sum("quantity"))["total"] or 0

    def get_total_price(self, cart: Cart) -> Decimal:
        """Calculates the total price of all items in the cart."""
        total = cart.cart_items.aggregate(
            total=Sum(F("quantity") * F("product__price"), output_field=DecimalField())
        )["total"]
        return total or Decimal("0.00")
