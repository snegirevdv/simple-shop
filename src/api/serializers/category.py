from rest_framework import serializers

from categories.models import Category, SubCategory


class SubCategoryReadSerializer(serializers.ModelSerializer):
    """Serializer for reading SubCategory instances."""

    class Meta:
        model = SubCategory
        fields = ("id", "name", "slug", "image")
        read_only_fields = fields


class CategoryReadSerializer(serializers.ModelSerializer):
    """Serializer for reading Category instances, including their subcategories."""

    subcategories = SubCategoryReadSerializer(many=True)

    class Meta:
        model = Category
        fields = ("id", "name", "slug", "image", "subcategories")
        read_only_fields = fields
