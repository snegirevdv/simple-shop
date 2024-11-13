from django.http import HttpRequest
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from cart.models import Cart, CartItem
from api.serializers.cart import CartReadSerializer, CartItemWriteSerializer


class CartAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def _get_cart(self) -> Cart:
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        return cart

    @extend_schema()
    def get(self, request, *args, **kwargs):
        cart = self._get_cart()
        serializer = CartReadSerializer(cart, context={"request": request})
        return Response(serializer.data)

    @extend_schema(request=CartItemWriteSerializer)
    def post(self, request: HttpRequest, *args, **kwargs):
        cart = self._get_cart()
        serializer = CartItemWriteSerializer(data=request.data, context={"cart": cart})

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        cart_item, created = CartItem.objects.get_or_create(
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

    def delete(self, request, *args, **kwargs):
        cart = self._get_cart()
        cart.cart_items.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartItemAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def _get_cart(self) -> Cart:
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        return cart

    @extend_schema(request=CartItemWriteSerializer)
    def put(self, request, pk=None, *args, **kwargs):
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

    def delete(self, request, pk=None, *args, **kwargs):
        cart = self._get_cart()
        cart_item = get_object_or_404(CartItem, pk=pk, cart=cart)
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
