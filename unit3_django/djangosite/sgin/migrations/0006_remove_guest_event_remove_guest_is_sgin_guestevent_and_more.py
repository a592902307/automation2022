# Generated by Django 4.1.3 on 2022-12-01 16:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sgin', '0005_event_starttime'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='guest',
            name='event',
        ),
        migrations.RemoveField(
            model_name='guest',
            name='is_sgin',
        ),
        migrations.CreateModel(
            name='GuestEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('join_time', models.DateTimeField(auto_now_add=True)),
                ('is_sgin', models.BooleanField(default=False)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sgin.event')),
                ('guest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sgin.guest')),
            ],
            options={
                'db_table': 'sgin_guest_events',
            },
        ),
        migrations.AddField(
            model_name='guest',
            name='events',
            field=models.ManyToManyField(through='sgin.GuestEvent', to='sgin.event'),
        ),
    ]