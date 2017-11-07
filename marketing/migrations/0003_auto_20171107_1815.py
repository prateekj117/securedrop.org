# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-07 18:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketing', '0002_auto_20171106_1518'),
    ]

    operations = [
        migrations.AddField(
            model_name='marketingindexpage',
            name='how_to_install_subtitle',
            field=models.CharField(blank=True, help_text='Appears immediately below subheader.', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='marketingindexpage',
            name='subtitle',
            field=models.CharField(blank=True, help_text='Appears immediately below page title.', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='marketingindexpage',
            name='subheader',
            field=models.CharField(default='How to install SecureDrop at your organization.', help_text='Displayed below features.', max_length=255),
        ),
    ]
