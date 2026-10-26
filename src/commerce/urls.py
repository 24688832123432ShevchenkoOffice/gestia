from django.urls import path

from src.commerce import views

urlpatterns = [
    path("koshik/", views.cart_page, name="cart"),
    path("koshik/dodaty/", views.cart_add, name="cart_add"),
    path("koshik/kilkist/", views.cart_update, name="cart_update"),
    path("zamovlennia/", views.checkout, name="checkout"),
    path("diakuiemo/", views.thanks, name="thanks"),
    path("zayavka/", views.callback, name="callback"),
    path("zamovyty-odrazu/", views.buy_now, name="buy_now"),
    path("zvorotnyi-zvyazok/", views.contact, name="contact"),
]
