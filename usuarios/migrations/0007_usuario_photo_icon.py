# Generated by Django 5.0.3 on 2024-03-30 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0006_remove_usuario_photo_icon'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='photo_icon',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
