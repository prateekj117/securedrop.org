# Generated by Django 2.2.12 on 2020-06-24 15:53

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0003_customimage_file_hash'),
    ]

    operations = [
        migrations.AlterField(
            model_name='footersettings',
            name='securedrop_onion_address',
            field=models.CharField(default='secrdrop5wyphb5x.onion', help_text='Address for the securedrop.org onion service. Displayed in the site footer and the Onion-Location header.  Must begin with http or https and end with .onion', max_length=255, validators=[django.core.validators.RegexValidator(message='Enter a valid .onion address.', regex='\\.onion$'), django.core.validators.URLValidator(message='Onion address must be a valid URL beginning with http or https', schemes=['http', 'https'])], verbose_name='SecureDrop Onion Address'),
        ),
    ]
