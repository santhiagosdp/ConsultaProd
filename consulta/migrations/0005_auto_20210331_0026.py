# Generated by Django 2.2.19 on 2021-03-31 03:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consulta', '0004_auto_20210331_0022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='dataCompra',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='produto',
            name='dataPublicacao',
            field=models.CharField(max_length=100),
        ),
    ]