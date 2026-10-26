from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from src.core.views import healthz, robots_txt, set_currency, set_language, theme_css

urlpatterns = [
    path("admin/", admin.site.urls),
    path("healthz/", healthz, name="healthz"),
    path("theme.css", theme_css, name="theme_css"),
    path("robots.txt", robots_txt, name="robots"),
    path("i18n/setlang/", set_language, name="set_language"),
    path("i18n/setcurrency/", set_currency, name="set_currency"),
]

urlpatterns += i18n_patterns(
    path("", include("src.core.urls")),
    prefix_default_language=False,
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
