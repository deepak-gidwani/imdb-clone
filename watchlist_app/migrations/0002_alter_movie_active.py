# Generated by Django 4.2 on 2023-04-04 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watchlist_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
