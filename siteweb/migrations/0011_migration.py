from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('bangri-agritech', '0010_ebook.py'),
    ]

    operations = [
        migrations.RunSQL("CREATE EXTENSION IF NOT EXISTS pg_trgm;"),
    ]
