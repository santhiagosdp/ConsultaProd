# Generated by Django 2.2.19 on 2021-03-31 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consulta', '0005_auto_20210331_0026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='dataPublicacao',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]