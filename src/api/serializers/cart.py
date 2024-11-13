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

    def create(self, validated_data: dict):
        cart = self.context["cart"]
        product = validated_data["product"]
        quantity = validated_data["quantity"]

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity

        cart_item.save()

        return cart_item

    def update(self, instance: CartItem, validated_data: dict):
        instance.quantity = validated_data.get("quantity", instance.quantity)
        instance.save()
        return instance


class CartReadSerializer(serializers.ModelSerializer):
    items = CartItemReadSerializer(many=True)
    total_quantity = serializers.IntegerField()
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Cart
        fields = ("id", "user", "items", "total_quantity", "total_price")
        read_only_fields = fields

    def get_total_quantity(self, obj: Cart):
        return sum(item.quantity for item in obj.cart_items.all())

    def get_total_price(self, obj: Cart):
        return sum(item.quantity * item.product.price for item in obj.cart_items.all())
