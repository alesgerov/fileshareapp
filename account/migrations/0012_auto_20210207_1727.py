# Generated by Django 3.1.3 on 2021-02-07 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_auto_20210207_1720'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ip',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]