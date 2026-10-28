from src.content.models import HomeBlock


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
