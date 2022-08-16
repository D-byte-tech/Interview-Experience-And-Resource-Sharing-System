# Generated by Django 4.0.2 on 2022-04-06 10:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Interview', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='interviewdatabase',
            name='userid',
        ),
        migrations.RemoveField(
            model_name='resourcedatabase',
            name='userid',
        ),
        migrations.AddField(
            model_name='interviewdatabase',
            name='Userid',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='resourcedatabase',
            name='Userid',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]