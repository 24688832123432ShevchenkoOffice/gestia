Основний шлях — Docker: `docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build`.

Без Docker, Ubuntu Droplet:

1. PostgreSQL: `sudo -u postgres createuser gestia && sudo -u postgres createdb -O gestia gestia`. Пароль — `ALTER USER`. У `.env`: `DATABASE_URL=postgres://gestia:ПАРОЛЬ@127.0.0.1:5432/gestia`, `DJANGO_SETTINGS_MODULE=config.settings.production`, `SECRET_KEY`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS=https://домен`.
2. Код у `/var/www/gestia`, `python3 -m venv .venv`, `pip install -r requirements.txt`, `python manage.py migrate`, `collectstatic`, `compilemessages`.
3. `sudo mkdir -p /run/gestia && sudo chown gestia:www-data /run/gestia`. Скопіювати `deploy/systemd/gunicorn.service` у `/etc/systemd/system/`, `systemctl enable --now gunicorn`.
4. Скопіювати `deploy/nginx/gestia.conf` у `/etc/nginx/sites-available/gestia`, підставити домен, `ln -s` у `sites-enabled`, `nginx -t && systemctl reload nginx`.
5. SSL: `sudo certbot --nginx -d домен -d www.домен`. Після сертифіката `SECURE_SSL_REDIRECT=True`.
6. Статику віддає nginx. WhiteNoise не використовується.
7. Сповіщення: `ORDER_NOTIFY_EMAIL`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`. Без них замовлення все одно зберігається.
