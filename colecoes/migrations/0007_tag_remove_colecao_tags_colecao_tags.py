# Generated by Django 5.0.3 on 2024-05-02 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('colecoes', '0006_busca'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='colecao',
            name='tags',
        ),
        migrations.AddField(
            model_name='colecao',
            name='tags',
            field=models.ManyToManyField(blank=True, to='colecoes.tag'),
        ),
    ]
