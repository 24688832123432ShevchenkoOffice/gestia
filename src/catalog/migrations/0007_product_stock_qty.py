from django.conf import settings
from django.db import migrations, models


def fill_placeholder_stock(apps, schema_editor):
    Product = apps.get_model("catalog", "Product")
    qty = settings.STOCK_PLACEHOLDER_QTY
    Product.objects.filter(stock_status__in=["in_stock", "on_order"]).update(stock_qty=qty)
    Product.objects.filter(stock_status="out").update(stock_qty=0)


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0006_figma_product"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="stock_qty",
            field=models.PositiveIntegerField(default=0, verbose_name="Залишок, шт"),
        ),
        migrations.RunPython(fill_placeholder_stock, migrations.RunPython.noop),
    ]
