"""Constants for the products app."""


class MaxLength:
    NAME = 255
    SLUG = 100


class ImageUploadPath:
    ORIGINAL = "products/original/"
    SMALL = "products/small/"
    MEDIUM = "products/medium/"
    LARGE = "products/large/"


class Price:
    MAX_DIGITS: int = 10
    DECIMAL_PLACES: int = 2


IMAGE_SIZES = {
    "small": (100, 100),
    "medium": (300, 300),
    "large": (600, 600),
}
