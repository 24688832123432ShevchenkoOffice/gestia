from django.db import migrations


PLACEHOLDER_QTY = 10


def set_placeholder_qty(apps, schema_editor):
    del schema_editor
    Product = apps.get_model("catalog", "Product")
    (
        Product.objects.filter(is_active=True)
        .exclude(stock_status="on_order")
        .update(stock_qty=PLACEHOLDER_QTY, stock_status="in_stock")
    )


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0014_product_is_sale"),
    ]

    operations = [
        migrations.RunPython(set_placeholder_qty, migrations.RunPython.noop),
    ]
