# Generated by Django 3.1.7 on 2021-04-08 13:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('consulta', '0012_auto_20210408_1012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]