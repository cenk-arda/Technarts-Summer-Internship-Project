# Generated by Django 3.1 on 2020-08-28 00:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0003_auto_20200827_0237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 28, 3, 17, 17, 604431)),
        ),
    ]
