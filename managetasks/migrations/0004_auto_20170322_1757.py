# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-22 17:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('managetasks', '0003_auto_20170322_1748'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pointscore',
            name='district_id',
            field=models.IntegerField(db_column='District', default=0),
        ),
    ]