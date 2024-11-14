from django.db import models

from categories import constants


class BaseCategory(models.Model):
    """Abstract base model for categories and subcategories."""

    name = models.CharField(
        max_length=constants.MaxLength.NAME,
        help_text="The name of the category",
    )
    slug = models.SlugField(
        max_length=constants.MaxLength.SLUG,
        unique=True,
        help_text="Unique slug for the category URL",
    )

    def __str__(self) -> str:
        return f"{self.name} (/{self.slug}/)"

    class Meta:
        abstract = True


class Category(BaseCategory):
    """Model representing a product category."""

    image = models.ImageField(upload_to="categories/")

    class Meta:
        ordering = ("name",)
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class SubCategory(BaseCategory):
    """Model representing a subcategory of a product category."""

    image = models.ImageField(
        upload_to="subcategories/",
        help_text="Image representing the subcategory",
    )
    category = models.ForeignKey(
        Category,
        related_name="subcategories",
        on_delete=models.CASCADE,
        help_text="Parent category",
    )

    class Meta:
        ordering = ("name",)
        verbose_name = "Subcategory"
        verbose_name_plural = "Subcategories"
