from django.http import HttpRequest
from rest_framework import serializers
from products.models import Product


class ProductReadSerializer(serializers.ModelSerializer):
    """Serializer for reading Product instances"""

    category = serializers.CharField(source="subcategory.category.name")
    subcategory = serializers.CharField(source="subcategory.name")
    images = serializers.SerializerMethodField()

    def get_images(self, obj: Product) -> dict[str, str]:
        """Generates absolute URLs for product images in different sizes."""
        request: HttpRequest = self.context["request"]

        return {
            "original": request.build_absolute_uri(obj.image.url),
            "small": request.build_absolute_uri(obj.image_small.url),
            "medium": request.build_absolute_uri(obj.image_medium.url),
            "large": request.build_absolute_uri(obj.image_large.url),
        }

    class Meta:
        model = Product
        fields = ("id", "name", "slug", "category", "subcategory", "price", "images")
        read_only_fields = fields
