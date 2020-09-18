# Generated by Django 3.1 on 2020-09-01 12:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('registration', '0002_myuser'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myuser',
            name='email',
        ),
        migrations.RemoveField(
            model_name='myuser',
            name='password',
        ),
        migrations.RemoveField(
            model_name='myuser',
            name='username',
        ),
        migrations.AddField(
            model_name='myuser',
            name='avatar',
            field=models.ImageField(null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='myuser',
            name='user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
            preserve_default=False,
        ),
    ]