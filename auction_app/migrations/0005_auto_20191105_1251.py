# Generated by Django 2.2.6 on 2019-11-05 19:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction_app', '0004_auto_20191105_1213'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='silentitem',
            name='start',
        ),
        migrations.AlterField(
            model_name='liveitem',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 5, 12, 51, 57, 658725), verbose_name=datetime.datetime(2019, 11, 5, 12, 51, 57, 658725)),
        ),
        migrations.AlterField(
            model_name='silentitem',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 5, 12, 51, 57, 658725), verbose_name=datetime.datetime(2019, 11, 5, 12, 51, 57, 658725)),
        ),
    ]