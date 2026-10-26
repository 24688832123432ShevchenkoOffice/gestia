from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from src.core.models import TimeStampedModel
from src.core.utils import localized

IMAGE_VALIDATOR = FileExtensionValidator(["jpg", "jpeg", "png", "webp"])


class Category(TimeStampedModel):
    parent = models.ForeignKey(
        "self",
        verbose_name="Батьківська категорія",
        null=True,
        blank=True,
        related_name="children",
        on_delete=models.CASCADE,
    )
    slug = models.SlugField("Слаг", max_length=80, unique=True)
    name_uk = models.CharField("Назва", max_length=160)
    name_ru = models.CharField("Назва (RU)", max_length=160, blank=True)
    name_en = models.CharField("Назва (EN)", max_length=160, blank=True)
    image = models.ImageField(
        "Зображення",
        upload_to="categories/",
        blank=True,
        validators=[IMAGE_VALIDATOR],
    )
    is_active = models.BooleanField("Активна", default=True)
    sort = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        ordering = ["sort", "name_uk"]
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"
        indexes = [models.Index(fields=["is_active", "sort"])]

    def __str__(self):
        return self.name_uk

    @property
    def name(self):
        return localized(self, "name")

    def get_absolute_url(self):
        return reverse("category", kwargs={"slug": self.slug})

    @property
    def has_public_products(self):
        if self.products.filter(is_active=True).exists():
            return True
        return self.children.filter(is_active=True, products__is_active=True).exists()

    def chain(self):
        nodes = []
        node = self
        seen = set()
        while node and node.pk not in seen:
            seen.add(node.pk)
            nodes.append(node)
            node = node.parent
        return list(reversed(nodes))


class ProductAttributeGroup(models.Model):
    class Slug(models.TextChoices):
        STYLE = "style", "Стиль"
        COLOR = "color", "Колір"

    slug = models.CharField("Слаг", max_length=32, choices=Slug.choices, unique=True)
    name_uk = models.CharField("Назва", max_length=80)
    name_ru = models.CharField("Назва (RU)", max_length=80, blank=True)
    name_en = models.CharField("Назва (EN)", max_length=80, blank=True)

    class Meta:
        verbose_name = "Група фільтра"
        verbose_name_plural = "Групи фільтрів"

    def __str__(self):
        return self.name_uk

    @property
    def name(self):
        return localized(self, "name")


class ProductAttribute(models.Model):
    group = models.ForeignKey(
        ProductAttributeGroup,
        verbose_name="Група",
        related_name="values",
        on_delete=models.CASCADE,
    )
    slug = models.SlugField("Слаг", max_length=80)
    name_uk = models.CharField("Назва", max_length=80)
    name_ru = models.CharField("Назва (RU)", max_length=80, blank=True)
    name_en = models.CharField("Назва (EN)", max_length=80, blank=True)
    is_filterable = models.BooleanField("У фільтрі", default=True)
    show_on_pdp = models.BooleanField("На картці", default=True)

    class Meta:
        verbose_name = "Значення фільтра"
        verbose_name_plural = "Значення фільтрів"
        constraints = [
            models.UniqueConstraint(fields=["group", "slug"], name="uniq_attr_group_slug")
        ]

    def __str__(self):
        return f"{self.group.name_uk}: {self.name_uk}"

    @property
    def name(self):
        return localized(self, "name")


class ProductSet(models.Model):
    slug = models.SlugField("Слаг", max_length=80, unique=True)
    name_uk = models.CharField("Назва", max_length=160)
    name_ru = models.CharField("Назва (RU)", max_length=160, blank=True)
    name_en = models.CharField("Назва (EN)", max_length=160, blank=True)

    class Meta:
        verbose_name = "Сет"
        verbose_name_plural = "Сети"

    def __str__(self):
        return self.name_uk

    @property
    def name(self):
        return localized(self, "name")


class Product(TimeStampedModel):
    class Stock(models.TextChoices):
        IN_STOCK = "in_stock", _("В наявності")
        ON_ORDER = "on_order", _("Під замовлення")
        OUT = "out", _("Немає в наявності")

    category = models.ForeignKey(
        Category,
        verbose_name="Категорія",
        related_name="products",
        on_delete=models.PROTECT,
    )
    product_set = models.ForeignKey(
        ProductSet,
        verbose_name="Сет",
        null=True,
        blank=True,
        related_name="products",
        on_delete=models.SET_NULL,
    )
    sku = models.CharField("Артикул", max_length=64, unique=True)
    slug = models.SlugField("Слаг", max_length=120, unique=True)
    name_uk = models.CharField("Назва", max_length=200)
    name_ru = models.CharField("Назва (RU)", max_length=200, blank=True)
    name_en = models.CharField("Назва (EN)", max_length=200, blank=True)
    description_uk = models.TextField("Опис", blank=True)
    description_ru = models.TextField("Опис (RU)", blank=True)
    description_en = models.TextField("Опис (EN)", blank=True)
    price_uah = models.DecimalField("Ціна, грн", max_digits=10, decimal_places=2)
    price_eur = models.DecimalField("Ціна, євро", max_digits=10, decimal_places=2)
    stock_status = models.CharField(
        "Наявність",
        max_length=16,
        choices=Stock.choices,
        default=Stock.IN_STOCK,
    )
    is_active = models.BooleanField("Активний", default=True)
    sort = models.PositiveIntegerField("Порядок", default=0)
    filter_attrs = models.ManyToManyField(
        ProductAttribute,
        verbose_name="Стиль і колір",
        blank=True,
        related_name="products",
    )
    related_manual = models.ManyToManyField(
        "self",
        verbose_name="Схожі вручну",
        blank=True,
        symmetrical=False,
        related_name="related_from",
    )
    seo_title_uk = models.CharField("SEO title", max_length=200, blank=True)
    seo_title_ru = models.CharField("SEO title (RU)", max_length=200, blank=True)
    seo_title_en = models.CharField("SEO title (EN)", max_length=200, blank=True)
    seo_description_uk = models.CharField("SEO description", max_length=300, blank=True)
    seo_description_ru = models.CharField("SEO description (RU)", max_length=300, blank=True)
    seo_description_en = models.CharField("SEO description (EN)", max_length=300, blank=True)

    class Meta:
        ordering = ["sort", "name_uk"]
        verbose_name = "Товар"
        verbose_name_plural = "Товари"
        indexes = [
            models.Index(fields=["is_active", "category"]),
            models.Index(fields=["sku"]),
        ]

    def __str__(self):
        return self.name_uk

    @property
    def name(self):
        return localized(self, "name")

    @property
    def description(self):
        return localized(self, "description")

    @property
    def seo_title(self):
        return localized(self, "seo_title") or self.name

    @property
    def seo_description(self):
        return localized(self, "seo_description") or self.description[:300]

    def amount(self, currency: str):
        if currency == "eur":
            return self.price_eur
        return self.price_uah

    def get_absolute_url(self):
        return reverse("product", kwargs={"slug": self.slug})

    @property
    def cover(self):
        cached = getattr(self, "_prefetched_objects_cache", {})
        if "images" in cached:
            images = list(cached["images"])
            return images[0] if images else None
        return self.images.order_by("sort", "id").first()


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        verbose_name="Товар",
        related_name="images",
        on_delete=models.CASCADE,
    )
    image = models.ImageField("Фото", upload_to="products/", validators=[IMAGE_VALIDATOR])
    sort = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        ordering = ["sort", "id"]
        verbose_name = "Фото товару"
        verbose_name_plural = "Фото товару"
