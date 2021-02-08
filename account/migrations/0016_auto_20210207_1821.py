# Generated by Django 3.1.3 on 2021-02-07 14:21

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0015_auto_20210207_1733'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='datetime',
        ),
        migrations.AddField(
            model_name='comment',
            name='date_comment',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='comment',
            name='date_edited',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='file',
            name='date_updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]