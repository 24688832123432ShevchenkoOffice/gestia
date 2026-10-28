from src.content.models import HomeBlock, SiteSettings
from src.content.models_legal import LegalPage


class HomeHeroBlock(HomeBlock):
    class Meta:
        proxy = True
        verbose_name = "Головний банер"
        verbose_name_plural = "Головний банер"


class HomeCategoriesBlock(HomeBlock):
    class Meta:
        proxy = True
        verbose_name = "Категорії"
        verbose_name_plural = "Категорії"


class HomeVideoBlock(HomeBlock):
    class Meta:
        proxy = True
        verbose_name = "Відео"
        verbose_name_plural = "Відео"


class HomePopularBlock(HomeBlock):
    class Meta:
        proxy = True
        verbose_name = "Популярні товари"
        verbose_name_plural = "Популярні товари"


class HomeAdvantagesBlock(HomeBlock):
    class Meta:
        proxy = True
        verbose_name = "Переваги"
        verbose_name_plural = "Переваги"


class HomeVideo2Block(HomeBlock):
    class Meta:
        proxy = True
        verbose_name = "Відео 2"
        verbose_name_plural = "Відео 2"


class HomeReviewsBlock(HomeBlock):
    class Meta:
        proxy = True
        verbose_name = "Відгуки"
        verbose_name_plural = "Відгуки"


class HomeCallbackBlock(HomeBlock):
    class Meta:
        proxy = True
        verbose_name = "Зворотний дзвінок"
        verbose_name_plural = "Зворотний дзвінок"


class OfferPage(LegalPage):
    class Meta:
        proxy = True
        verbose_name = "Публічний договір"
        verbose_name_plural = "Публічний договір"


class PrivacyPolicyPage(LegalPage):
    class Meta:
        proxy = True
        verbose_name = "Політика конфіденційності"
        verbose_name_plural = "Політика конфіденційності"


class CookiePolicyPage(LegalPage):
    class Meta:
        proxy = True
        verbose_name = "Політика cookies"
        verbose_name_plural = "Політика cookies"


class ShippingPage(LegalPage):
    class Meta:
        proxy = True
        verbose_name = "Доставка та оплата"
        verbose_name_plural = "Доставка та оплата"


class FooterChrome(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = "Тексти підвалу"
        verbose_name_plural = "Тексти підвалу"
