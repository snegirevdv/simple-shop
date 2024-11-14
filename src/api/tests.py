from decimal import Decimal
import io

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from PIL import Image

from cart.models import Cart, CartItem
from categories.models import Category, SubCategory
from products.models import Product

User = get_user_model()


def get_temporary_image(name: str) -> SimpleUploadedFile:
    image = Image.new("RGB", (100, 100), color=(255, 0, 0))
    byte_arr = io.BytesIO()
    image.save(byte_arr, format="JPEG")
    byte_arr.seek(0)
    return SimpleUploadedFile(name, byte_arr.read(), content_type="image/jpeg")


class CartAPITestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category_image = get_temporary_image("category.jpg")
        cls.category = Category.objects.create(
            name="Category 1",
            image=cls.category_image,
        )

        cls.subcategory_image = get_temporary_image("subcategory.jpg")
        cls.subcategory = SubCategory.objects.create(
            name="Subcategory 1",
            category=cls.category,
            image=cls.subcategory_image,
        )

        cls.product_image = get_temporary_image("product1.jpg")
        cls.product = Product.objects.create(
            name="Product 1",
            price=Decimal("100.00"),
            slug="product-one",
            subcategory=cls.subcategory,
            image=cls.product_image,
        )

        cls.product2_image = get_temporary_image("product2.jpg")
        cls.product2 = Product.objects.create(
            name="Another Product",
            price=Decimal("150.28"),
            slug="product-two",
            subcategory=cls.subcategory,
            image=cls.product2_image,
        )

        cls.cart_url = reverse("cart")

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="password123",
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_empty_cart(self):
        """Verify the cart is empty when no items have been added."""
        response = self.client.get(self.cart_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_quantity"], 0)
        self.assertEqual(response.data["total_price"], 0)
        self.assertEqual(response.data["items"], [])

    def test_total_price_and_quantity_calculation(self):
        """Verify total price and quantity calculation."""
        self.client.post(self.cart_url, {"product": self.product.pk, "quantity": 2})
        self.client.post(self.cart_url, {"product": self.product2.pk, "quantity": 3})
        response = self.client.get(self.cart_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_quantity"], 5)
        self.assertEqual(
            response.data["total_price"],
            Decimal("2") * self.product.price + Decimal("3") * self.product2.price,
        )

    def test_add_product_to_cart(self):
        """Ensure a product can be successfully added to the cart."""
        data = {"product": self.product.pk, "quantity": 2}
        response = self.client.post(self.cart_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        cart = Cart.objects.get(user=self.user)
        cart_item = CartItem.objects.get(cart=cart, product=self.product)
        self.assertEqual(cart_item.quantity, 2)

    def test_add_same_product_increments_quantity(self):
        """Ensure adding the same product increments its quantity in the cart."""
        data = {"product": self.product.pk, "quantity": 1}
        self.client.post(self.cart_url, data)

        response = self.client.post(self.cart_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        cart = Cart.objects.get(user=self.user)
        cart_item = CartItem.objects.get(cart=cart, product=self.product)
        self.assertEqual(cart_item.quantity, 2)

    def test_get_cart_unauthorized(self):
        """Check that an unauthorized user cannot access the cart endpoint."""
        self.client.credentials()
        response = self.client.get(self.cart_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_add_product_to_cart_invalid_quantity(self):
        """Check that a user cannot add incorrect quantity of the product."""
        data = {"product": self.product.pk, "quantity": -1}
        response = self.client.post(self.cart_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("quantity", response.data)

    def test_update_nonexistent_cart_item(self):
        """Check updating a non-existent cart item."""
        data = {"quantity": 5}
        response = self.client.put(reverse("cart-item", args=(10**1000,)), data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
