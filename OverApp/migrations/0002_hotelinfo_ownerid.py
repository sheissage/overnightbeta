# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-05-26 15:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
       
    ]

    operations = [
        migrations.AddField(
            model_name='hotelInfo',
            name='ownerId',
            field=models.TextField(db_column='owner', default='Overnightasia'),
        ),
    ]
