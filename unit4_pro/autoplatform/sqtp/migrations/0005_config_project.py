# Generated by Django 4.1.4 on 2023-02-27 14:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("sqtp", "0004_alter_user_user_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="config",
            name="project",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="sqtp.project",
            ),
        ),
    ]
