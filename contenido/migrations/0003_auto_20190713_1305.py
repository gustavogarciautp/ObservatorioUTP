# Generated by Django 2.2 on 2019-07-13 18:05

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenido', '0002_auto_20190713_1120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='noticia',
            name='descripcion',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
    ]