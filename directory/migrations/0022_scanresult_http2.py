# Generated by Django 2.2.14 on 2020-09-08 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('directory', '0021_merge_20200903_1933'),
    ]

    operations = [
        migrations.AddField(
            model_name='scanresult',
            name='http2',
            field=models.BooleanField(default=False),
        ),
    ]
