# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-28 20:38
from __future__ import unicode_literals

import django.contrib.auth.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20170328_1847'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='height',
            field=models.IntegerField(default=0, verbose_name='\u0420\u043e\u0441\u0442'),
        ),
    ]
