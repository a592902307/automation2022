# Generated by Django 4.1.3 on 2022-11-23 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sgin', '0003_guest'),
    ]

    operations = [
        migrations.AddField(
            model_name='guest',
            name='is_sgin',
            field=models.BooleanField(default=False),
        ),
    ]
