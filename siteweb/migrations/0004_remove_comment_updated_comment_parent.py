# Generated by Django 5.1.1 on 2024-09-28 03:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('siteweb', '0003_subscriber'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='updated',
        ),
        migrations.AddField(
            model_name='comment',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='siteweb.comment'),
        ),
    ]
