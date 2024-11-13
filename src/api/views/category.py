from rest_framework import viewsets

from api.serializers.category import CategoryReadSerializer
from categories.models import Category


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all().prefetch_related("subcategories")
    serializer_class = CategoryReadSerializer
