from urllib.parse import urlparse

from decouple import config

from .base import *  # noqa: F403

DEBUG = False

_db = urlparse(config("DATABASE_URL"))
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": _db.path.lstrip("/"),
        "USER": _db.username,
        "PASSWORD": _db.password,
        "HOST": _db.hostname,
        "PORT": _db.port or 5432,
        "CONN_MAX_AGE": 60,
    }
}

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
# Lax keeps the cart session on the first top-level visit from Instagram,
# Telegram, or Google. Strict dropped the cookie on that cross-site GET.
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SAMESITE = "Strict"
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_SSL_REDIRECT = config("SECURE_SSL_REDIRECT", default=False, cast=bool)
CSRF_TRUSTED_ORIGINS = config(
    "CSRF_TRUSTED_ORIGINS",
    default="",
    cast=lambda v: [s.strip() for s in v.split(",") if s.strip()],
)
