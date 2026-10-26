from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from src.catalog.models import Category, Product
from src.commerce.forms import ContactForm, style_form
from src.commerce.models import Inquiry
from src.commerce.services import create_inquiry
from src.content.models import AboutPage, Advantage, PrivacyPage, Review


@require_http_methods(["GET", "POST"])
def home(request):
    form = style_form(ContactForm(request.POST or None))
    if request.method == "POST" and form.is_valid():
        create_inquiry(
            kind=Inquiry.Kind.CONTACT,
            name=form.cleaned_data["name"],
            phone=form.cleaned_data["phone"],
            message=form.cleaned_data["message"],
            consent=True,
        )
        return redirect(f"{reverse('thanks')}?kind=contact")
    categories = Category.objects.filter(is_active=True, home_sort__isnull=False).order_by("home_sort", "id")
    popular = (
        Product.objects.filter(is_active=True, is_popular=True)
        .prefetch_related("images")
        .order_by("sort", "id")
    )
    return render(
        request,
        "content/home.html",
        {
            "categories": categories,
            "popular": popular,
            "advantages": Advantage.objects.all(),
            "reviews": Review.objects.all(),
            "home_form": form,
        },
    )


def about(request):
    page = AboutPage.load()
    return render(request, "content/about.html", {"page": page})


def privacy(request):
    page = PrivacyPage.load()
    return render(request, "content/privacy.html", {"page": page})
