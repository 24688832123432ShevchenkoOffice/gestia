from django.urls import path

from src.content import views

urlpatterns = [
    path("", views.home, name="home"),
    path("pro-nas/", views.about, name="about"),
    path("publichnyi-dogovir/", views.offer, name="offer"),
    path("polityka-konfidentsiynosti/", views.privacy, name="privacy"),
    path("polityka-cookies/", views.cookies, name="cookies"),
]
