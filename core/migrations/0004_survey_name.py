# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-19 18:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_diary_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='name',
            field=models.CharField(default='', max_length=200, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u043e\u043f\u0440\u043e\u0441\u0430'),
        ),
    ]
