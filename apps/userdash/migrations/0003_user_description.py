# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-18 02:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userdash', '0002_message_addressee'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='description',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
