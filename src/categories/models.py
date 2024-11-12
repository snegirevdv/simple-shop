from django.db import models


class BaseCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def __str__(self) -> str:
        return f"{self.name} (/{self.slug}/)"

    class Meta:
        abstract = True


class Category(BaseCategory):
    image = models.ImageField(upload_to="categories/")


class SubCategory(BaseCategory):
    image = models.ImageField(upload_to="subcategories/")
    category = models.ForeignKey(
        Category,
        related_name="subcategories",
        on_delete=models.CASCADE,
    )
