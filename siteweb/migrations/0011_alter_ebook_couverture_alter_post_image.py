# Generated by Django 5.1.1 on 2024-12-11 05:29

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('siteweb', '0010_ebook'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ebook',
            name='couverture',
            field=cloudinary.models.CloudinaryField(default=1, max_length=255, verbose_name='couverture'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='post',
            name='image',
            field=cloudinary.models.CloudinaryField(default=1, max_length=255, verbose_name='image'),
            preserve_default=False,
        ),
    ]
