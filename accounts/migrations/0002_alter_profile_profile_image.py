# Generated by Django 4.1.7 on 2023-03-24 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(blank=True, default='profile_images/profile_pic.jpg', null=True, upload_to=''),
        ),
    ]
