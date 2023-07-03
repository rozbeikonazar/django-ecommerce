# Generated by Django 4.1.7 on 2023-07-01 20:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_alter_category_name_alter_product_description_and_more'),
        ('cart', '0003_alter_orderitem_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, to='products.product'),
            preserve_default=False,
        ),
    ]