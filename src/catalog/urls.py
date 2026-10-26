from django.urls import path

from src.catalog import views

urlpatterns = [
    path("katalog/", views.catalog, name="catalog"),
    path("katalog/<slug:slug>/", views.catalog, name="category"),
    path("tovar/<slug:slug>/", views.product_detail, name="product"),
]
