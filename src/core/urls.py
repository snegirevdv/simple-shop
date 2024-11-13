from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views.product import ProductViewSet
from api.views.category import CategoryViewSet
from api.views.cart import CartAPIView, CartItemAPIView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


router = DefaultRouter()
router.register(r"products", ProductViewSet, basename="product")
router.register(r"categories", CategoryViewSet, basename="category")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/auth/", include("djoser.urls.authtoken")),
    path("api/cart/", CartAPIView.as_view(), name="cart"),
    path("api/cart/<int:pk>/", CartItemAPIView.as_view(), name="cart-item"),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]
