# Generated by Django 5.1.1 on 2024-09-30 10:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Profile',
        ),
    ]