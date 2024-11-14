from django.db import models
from django.contrib.auth import get_user_model

from cart.constants import DEFAULT_QUANTITY
from products.models import Product

User = get_user_model()


class Cart(models.Model):
    """Represents a shopping cart associated with a user."""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="shopping_cart",
    )

    def __str__(self) -> str:
        return f"Cart of {self.user.username}"


class CartItem(models.Model):
    """Represents an item in the shopping cart."""

    cart = models.ForeignKey(Cart, related_name="cart_items", on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product,
        related_name="in_carts",
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveIntegerField(
        default=DEFAULT_QUANTITY,
        help_text="Quantity of the product in the cart.",
    )

    def __str__(self) -> str:
        return f"{self.product.name} - {self.quantity}"
