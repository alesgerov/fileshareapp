# Generated by Django 3.1.3 on 2021-02-05 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_auto_20210205_0133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ip',
            name='pub_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]