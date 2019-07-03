# Generated by Django 2.2 on 2019-07-03 15:01

import app_core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_core', '0006_auto_20190701_1522'),
    ]

    operations = [
        migrations.AddField(
            model_name='egresado',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to=app_core.models.custom_upload_to),
        ),
        migrations.AddField(
            model_name='egresado',
            name='avatar_p',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='egresado',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='egresado',
            name='bio_p',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='egresado',
            name='email_p',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='egresado',
            name='fecha_p',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='egresado',
            name='nombres_p',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='egresado',
            name='pais_p',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='egresado',
            name='activacion',
            field=models.BooleanField(default=False, null=True, verbose_name='Activacion'),
        ),
    ]