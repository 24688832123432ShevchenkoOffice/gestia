from pathlib import Path

from decouple import Csv, config

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = config("SECRET_KEY")

DEBUG = False

ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="", cast=Csv())

INSTALLED_APPS = [
    "unfold",
    "unfold.contrib.forms",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "tinymce",
    "src.core",
    "src.content",
    "src.catalog",
    "src.commerce",
]

MIDDLEWARE = [
    "src.core.middleware.ContentSecurityPolicyMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "src.core.middleware.AdminUkrainianMiddleware",
    "src.core.middleware.LanguagePrefixMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.i18n",
                "src.core.context_processors.shop",
            ],
        },
    }
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
        "OPTIONS": {
            "transaction_mode": "IMMEDIATE",
            "timeout": 20,
        },
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "uk"
LANGUAGES = [
    ("uk", "Українська"),
    ("en", "English"),
]
LOCALE_PATHS = [BASE_DIR / "locale"]
TIME_ZONE = "Europe/Kyiv"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = []
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default="shop@example.com")
ORDER_NOTIFY_EMAIL = config("ORDER_NOTIFY_EMAIL", default="")
TELEGRAM_BOT_TOKEN = config("TELEGRAM_BOT_TOKEN", default="")
TELEGRAM_CHAT_ID = config("TELEGRAM_CHAT_ID", default="")
NOVA_POSHTA_API_KEY = config("NOVA_POSHTA_API_KEY", default="")

# Тимчасова кількість для товарів, які вже були в наявності або під замовлення.
# Адміністратор має замінити її на реальний залишок кожної позиції.
STOCK_PLACEHOLDER_QTY = 100

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "gestia",
    }
}

# Per-form overrides use the same shape. Missing keys fall back to "default".
RATE_LIMITS = {
    "default": {"limit": 5, "window": 600},
}
TRUST_X_FORWARDED_FOR = config("TRUST_X_FORWARDED_FOR", default=False, cast=bool)


def _normalize_admin_url(raw: str) -> str:
    value = str(raw or "").strip().strip("/")
    if not value:
        return "admin/"
    return f"{value}/"


ADMIN_URL = _normalize_admin_url(config("ADMIN_URL", default="admin/"))

# Public pages load Google Fonts and have no inline scripts or map iframes.
CSP_REPORT_ONLY = config("CSP_REPORT_ONLY", default=True, cast=bool)
CSP_POLICY = "; ".join(
    [
        "default-src 'self'",
        "base-uri 'self'",
        "form-action 'self'",
        "frame-ancestors 'none'",
        "script-src 'self'",
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com",
        "font-src 'self' https://fonts.gstatic.com",
        "img-src 'self' data: https:",
        "connect-src 'self' https://fonts.googleapis.com https://fonts.gstatic.com",
    ]
)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {"format": "{levelname} {asctime} {module} {message}", "style": "{"},
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "verbose"},
    },
    "root": {"handlers": ["console"], "level": "WARNING"},
    "loggers": {
        "django.request": {"handlers": ["console"], "level": "ERROR", "propagate": False},
        "src": {"handlers": ["console"], "level": "INFO", "propagate": False},
    },
}

def _admin_asset(path):
    def href(request):
        from django.templatetags.static import static

        return static(path)

    return href


TINYMCE_DEFAULT_CONFIG = {
    "height": 280,
    "menubar": False,
    "branding": False,
    "promotion": False,
    "statusbar": False,
    "plugins": "link lists",
    "toolbar": (
        "undo redo | bold italic underline | bullist numlist | link | "
        "blocks | blockquote | removeformat"
    ),
    "block_formats": "Абзац=p; Заголовок 2=h2; Заголовок 3=h3; Заголовок 4=h4",
    "language": "uk",
    "forced_root_block": "p",
    "newline_behavior": "block",
    "valid_elements": (
        "p,br,strong/b,em/i,u,a[href|target|rel],ul,ol,li,h2,h3,h4,blockquote,span"
    ),
    "link_default_target": "_blank",
    "link_default_rel": "noopener noreferrer",
    "content_style": (
        "body { font-family: -apple-system, BlinkMacSystemFont, sans-serif; "
        "font-size: 16px; line-height: 1.5; margin: 8px; }"
        "p { margin: 0 0 0.75em; }"
    ),
}

UNFOLD = {
    "SITE_TITLE": "Gestia Home",
    "SITE_HEADER": "Gestia Home",
    "SITE_SYMBOL": "storefront",
    "SITE_URL": "/",
    "SHOW_HISTORY": True,
    "SHOW_LANGUAGES": False,
    "STYLES": [
        _admin_asset("css/admin/char_counter.css"),
        _admin_asset("css/admin/image_preview.css"),
    ],
    "SCRIPTS": [
        _admin_asset("js/admin/char_counter.js"),
    ],
    "COLORS": {
        "base": {
            "50": "#faf7f2",
            "100": "#f3eee6",
            "200": "#e7e0d4",
            "300": "#d9cfc2",
            "400": "#b5a89a",
            "500": "#8c7f72",
            "600": "#5c5148",
            "700": "#3d342c",
            "800": "#2c241e",
            "900": "#241c16",
            "950": "#16110e",
        },
        "primary": {
            "50": "#fbf6f4",
            "100": "#f6ece8",
            "200": "#ead5ce",
            "300": "#d7b0a4",
            "400": "#c07a68",
            "500": "#a4513c",
            "600": "#8d3b2a",
            "700": "#743022",
            "800": "#5c261b",
            "900": "#4a1f16",
            "950": "#2c120d",
        },
    },
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": False,
        "navigation": "src.core.admin_nav.build_navigation",
    },
}
