# Generated by Django 3.1.7 on 2021-05-13 13:12

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('consulta', '0009_auto_20210505_1121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acesso',
            name='data',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 13, 13, 12, 20, 948204, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='produto',
            name='data',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 13, 13, 12, 20, 948204, tzinfo=utc)),
        ),
    ]