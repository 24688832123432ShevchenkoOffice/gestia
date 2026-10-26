from django.urls import path

from src.content import views

urlpatterns = [
    path("", views.home, name="home"),
    path("pro-nas/", views.about, name="about"),
    path("polityka-konfidentsiynosti/", views.privacy, name="privacy"),
]
