from rest_framework import serializers

from categories.models import Category, SubCategory


class SubCategoryReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ("id", "name", "slug", "image")
        read_only_fields = fields


class CategoryReadSerializer(serializers.ModelSerializer):
    subcategories = SubCategoryReadSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ("id", "name", "slug", "image", "subcategories")
