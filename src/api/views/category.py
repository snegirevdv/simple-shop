from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets

from api.serializers.category import CategoryReadSerializer
from categories.models import Category


@extend_schema_view(
    list=extend_schema(
        summary="Get category list",
        description="Returns a list of all categories with their subcategories.",
    ),
)
class CategoryViewSet(viewsets.mixins.ListModelMixin, viewsets.GenericViewSet):
    """API endpoint that allows categories to be viewed."""

    queryset = Category.objects.all().prefetch_related("subcategories")
    serializer_class = CategoryReadSerializer
