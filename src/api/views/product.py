from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets

from api.serializers.product import ProductReadSerializer
from products.models import Product


@extend_schema_view(
    list=extend_schema(
        summary="Get product list",
        description="Returns a list of all products with their subcategories and categories.",
    ),
)
class ProductViewSet(viewsets.mixins.ListModelMixin, viewsets.GenericViewSet):
    """API endpoint that allows products to be viewed."""

    queryset = Product.objects.all().select_related("subcategory__category")
    serializer_class = ProductReadSerializer
