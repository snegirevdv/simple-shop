import os
from typing import override

from django.conf import settings
from django.db import models
from PIL import Image

from categories.models import SubCategory


class Product(models.Model):
    subcategory = models.ForeignKey(
        SubCategory,
        related_name="products",
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to="products/original/")
    image_small = models.ImageField(upload_to="products/small/", null=True, blank=True)
    image_medium = models.ImageField(
        upload_to="products/medium/",
        null=True,
        blank=True,
    )
    image_large = models.ImageField(upload_to="products/large/", null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    @override
    def save(self, *args, **kwargs) -> None:
        super().save(*args, **kwargs)
        self.create_images()

    def create_images(self) -> None:
        """Creates small, medium, and large versions of the product image."""
        sizes = {
            "small": (100, 100),
            "medium": (300, 300),
            "large": (600, 600),
        }

        original_image = Image.open(self.image.path)

        for size_name, size in sizes.items():
            image = original_image.copy()
            image.thumbnail(size)

            image_name = os.path.basename(self.image.name)
            base_name, ext = os.path.splitext(image_name)

            file_name = f"{base_name}_{size_name}{ext}"
            base_path = os.path.join("products", size_name, file_name)
            full_path = os.path.join(settings.MEDIA_ROOT, base_path)

            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            image.save(full_path)

            setattr(self, f"image_{size_name}", base_path)

        super().save(update_fields=[f"image_{size_name}" for size_name in sizes.keys()])

    def __str__(self) -> str:
        return self.name
