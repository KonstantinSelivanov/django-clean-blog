# Generated by Django 3.1.4 on 2020-12-19 19:42

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('publications', '0014_auto_20201219_1923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='body',
            field=ckeditor.fields.RichTextField(verbose_name='Коментарий'),
        ),
    ]