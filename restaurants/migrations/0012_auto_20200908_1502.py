# Generated by Django 3.1 on 2020-09-08 12:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0011_auto_20200908_1438'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 8, 15, 2, 28, 618006)),
        ),
    ]