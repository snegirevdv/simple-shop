from django.http import HttpRequest
from rest_framework import serializers
from products.models import Product


class ProductReadSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="subcategory.category.name")
    subcategory = serializers.CharField(source="subcategory.name")
    images = serializers.SerializerMethodField()

    def get_images(self, obj: Product) -> dict[str, str]:
        request: HttpRequest = self.context.get("request")

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
