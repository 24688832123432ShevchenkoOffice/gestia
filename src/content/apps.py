from django.apps import AppConfig


class ContentConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "src.content"
    verbose_name = "Вміст сайту"

    def ready(self):
        from src.content import proxies as _home_proxies  # noqa: F401
