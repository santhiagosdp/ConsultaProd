# Generated by Django 3.1.7 on 2021-05-05 14:14

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('consulta', '0004_produto_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='acesso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200)),
                ('data', models.DateTimeField(default=datetime.datetime(2021, 5, 5, 14, 14, 53, 517138, tzinfo=utc))),
            ],
        ),
        migrations.AlterField(
            model_name='produto',
            name='data',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 5, 14, 14, 53, 517138, tzinfo=utc)),
        ),
    ]
