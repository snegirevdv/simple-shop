from rest_framework import viewsets

from api.serializers.product import ProductReadSerializer
from products.models import Product


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all().select_related("subcategory__category")
    serializer_class = ProductReadSerializer
