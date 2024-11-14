import os

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models, transaction
from PIL import Image

from categories.models import SubCategory
from products.constants import MaxLength, ImageUploadPath, IMAGE_SIZES, Price


class Product(models.Model):
    """Model representing a product."""

    subcategory = models.ForeignKey(
        SubCategory,
        related_name="products",
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        max_length=MaxLength.NAME,
        help_text="The name of the product.",
    )
    slug = models.SlugField(
        unique=True,
        max_length=MaxLength.SLUG,
        help_text="Unique slug for the product URL.",
    )
    image = models.ImageField(
        upload_to=ImageUploadPath.ORIGINAL,
        help_text="Original image of the product.",
    )
    image_small = models.ImageField(
        upload_to=ImageUploadPath.SMALL,
        null=True,
        blank=True,
        help_text="Small version of the product image.",
    )
    image_medium = models.ImageField(
        upload_to=ImageUploadPath.MEDIUM,
        null=True,
        blank=True,
        help_text="Medium version of the product image.",
    )
    image_large = models.ImageField(
        upload_to=ImageUploadPath.LARGE,
        null=True,
        blank=True,
        help_text="Large version of the product image.",
    )
    price = models.DecimalField(
        max_digits=Price.MAX_DIGITS,
        decimal_places=Price.DECIMAL_PLACES,
        validators=[MinValueValidator(0)],
        help_text="Price of the product.",
    )

    @transaction.atomic
    def save(self, *args, **kwargs) -> None:
        super().save(*args, **kwargs)
        self.create_images()
        super().save(
            update_fields=[f"image_{size_name}" for size_name in IMAGE_SIZES.keys()]
        )

    def delete(self, *args, **kwargs):
        for image in (
            self.image,
            self.image_small,
            self.image_medium,
            self.image_large,
        ):
            storage = image.storage

            if storage.exists(image.name):
                storage.delete(image.name)

        super().delete(*args, **kwargs)

    def __str__(self) -> str:
        return self.name

    def create_images(self) -> None:
        """Creates small, medium, and large versions of the product image."""

        original_image = Image.open(self.image.path)

        for size_name, size in IMAGE_SIZES.items():
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
