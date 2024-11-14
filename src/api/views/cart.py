from django.http import HttpRequest, HttpResponse
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from cart.models import Cart, CartItem
from api.serializers.cart import CartReadSerializer, CartItemWriteSerializer


class CartAPIView(APIView):
    """API view for retrieving, adding to, and clearing the user's cart."""

    permission_classes = (permissions.IsAuthenticated,)

    def _get_cart(self) -> Cart:
        """Retrieves the cart for the authenticated user, creating one if it doesn't exist."""
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        return cart

    @extend_schema(
        summary="Get shopping cart items",
        description="Returns the contents of the current user's shopping cart.",
    )
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """Retrieves the authenticated user's cart with items, total quantity, and total price."""
        cart = self._get_cart()
        serializer = CartReadSerializer(cart, context={"request": request})
        return Response(serializer.data)

    @extend_schema(
        summary="Add an item to the shopping cart",
        description="Adds an item to the cart or updates its quantity if it already exists.",
        request=CartItemWriteSerializer,
    )
    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """Adds a product to the cart or updates the quantity if it already exists."""
        cart = self._get_cart()
        serializer = CartItemWriteSerializer(data=request.data, context={"cart": cart})

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        cart_item, created = CartItem.objects.select_for_update().get_or_create(
            cart=cart,
            product=serializer.validated_data["product"],
        )

        if created:
            cart_item.quantity = serializer.validated_data["quantity"]
        else:
            cart_item.quantity += serializer.validated_data["quantity"]

        cart_item.save()

        return Response(
            CartReadSerializer(cart, context={"request": request}).data,
            status=status.HTTP_201_CREATED,
        )

    @extend_schema(
        summary="Clear a shopping cart",
        description="Removes all items from the current user's cart.",
    )
    def delete(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """Clears all items from the authenticated user's cart."""
        cart = self._get_cart()
        cart.cart_items.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartItemAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def _get_cart(self) -> Cart:
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        return cart

    @extend_schema(
        summary="Update quantity of the item",
        description="Changes the quantity of the specified item in the cart.",
        request=CartItemWriteSerializer,
    )
    def put(
        self,
        request: HttpRequest,
        pk: int | None = None,
        *args,
        **kwargs,
    ) -> HttpResponse:
        cart = self._get_cart()
        cart_item = get_object_or_404(CartItem, pk=pk, cart=cart)

        serializer = CartItemWriteSerializer(
            cart_item,
            data=request.data,
            partial=False,
            context={"cart": cart},
        )

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        cart_item.quantity = serializer.validated_data["quantity"]
        cart_item.save()
        return Response(CartReadSerializer(cart, context={"request": request}).data)

    @extend_schema(
        summary="Remove item from the cart",
        description="Removes the specified item from the current user's cart.",
    )
    def delete(self, request, pk=None, *args, **kwargs) -> HttpResponse:
        """Deletes a specific item from the authenticated user's cart."""
        cart = self._get_cart()
        cart_item = get_object_or_404(CartItem, pk=pk, cart=cart)
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
