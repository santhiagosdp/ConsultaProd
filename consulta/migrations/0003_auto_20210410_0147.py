# Generated by Django 3.1.7 on 2021-04-10 04:47

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('consulta', '0002_remove_nota_datapublicacao'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emitente',
            name='dataPublicacao',
        ),
        migrations.AddField(
            model_name='emitente',
            name='publicacao',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AddField(
            model_name='nota',
            name='publicacao',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
    ]
