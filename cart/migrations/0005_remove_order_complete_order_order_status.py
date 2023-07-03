# Generated by Django 4.1.7 on 2023-07-03 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0004_alter_orderitem_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='complete',
        ),
        migrations.AddField(
            model_name='order',
            name='order_status',
            field=models.BooleanField(choices=[('cart', 'Cart'), ('pending', 'Pending'), ('processing', 'Processing'), ('shipped', 'Shipped'), ('delivered', 'Delivered'), ('cancelled', 'Cancelled')], default=False, max_length=50),
        ),
    ]