# Generated by Django 5.0.3 on 2024-03-29 03:24

import usuarios.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='photo',
            field=models.ImageField(blank=True, upload_to=usuarios.models.upload_to),
        ),
    ]
