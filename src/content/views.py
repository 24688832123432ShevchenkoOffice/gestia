from django.shortcuts import render

from src.catalog.models import Category
from src.content.models import AboutPage, Advantage, PrivacyPage


def home(request):
    categories = (
        Category.objects.filter(parent__isnull=True, is_active=True)
        .prefetch_related("children")
        .order_by("sort", "name_uk")
    )
    visible = [cat for cat in categories if cat.has_public_products]
    return render(
        request,
        "content/home.html",
        {"categories": visible, "advantages": Advantage.objects.all()},
    )


def about(request):
    page = AboutPage.load()
    return render(request, "content/about.html", {"page": page})


def privacy(request):
    page = PrivacyPage.load()
    return render(request, "content/privacy.html", {"page": page})
