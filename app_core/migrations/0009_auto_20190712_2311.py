# Generated by Django 2.2 on 2019-07-13 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_core', '0008_egresado_ciudad_p'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interes',
            name='nombre',
            field=models.CharField(default='', max_length=30, unique=True, verbose_name='Nombre'),
        ),
    ]
