from rest_framework import viewsets

from api.serializers.category import CategoryReadSerializer
from categories.models import Category


class CategoryViewSet(viewsets.mixins.ListModelMixin, viewsets.GenericViewSet):
    """API endpoint that allows categories to be viewed."""

    queryset = Category.objects.all().prefetch_related("subcategories")
    serializer_class = CategoryReadSerializer
