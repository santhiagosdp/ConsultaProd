# Generated by Django 3.1.7 on 2021-04-12 00:27

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('consulta', '0003_auto_20210410_0147'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='data',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 12, 0, 27, 40, 864813, tzinfo=utc)),
        ),
    ]
