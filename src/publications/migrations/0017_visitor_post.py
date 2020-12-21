# Generated by Django 3.1.4 on 2020-12-20 18:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('publications', '0016_auto_20201220_1627'),
    ]

    operations = [
        migrations.AddField(
            model_name='visitor',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='visitor_publications', to='publications.post', verbose_name='Пост'),
            preserve_default=False,
        ),
    ]
