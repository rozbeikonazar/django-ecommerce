# Generated by Django 4.1.7 on 2023-07-06 18:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0010_alter_cartitem_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippingaddress',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cart.order'),
        ),
    ]