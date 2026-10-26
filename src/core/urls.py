from django.urls import include, path

urlpatterns = [
    path("", include("src.content.urls")),
    path("", include("src.catalog.urls")),
    path("", include("src.commerce.urls")),
]
