# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-22 17:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('managetasks', '0002_auto_20170322_1711'),
    ]

    operations = [
        migrations.AddField(
            model_name='pointscore',
            name='added_time',
            field=models.DateTimeField(auto_now_add=True, db_column='addedTime', default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pointscore',
            name='auto_id',
            field=models.IntegerField(db_column='AutoID', default=0),
        ),
        migrations.AddField(
            model_name='pointscore',
            name='block_num',
            field=models.IntegerField(db_column='Block', default=0),
        ),
        migrations.AddField(
            model_name='pointscore',
            name='district_id',
            field=models.IntegerField(db_column='District', default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pointscore',
            name='district_name',
            field=models.CharField(db_column='DisName', default='', max_length=30),
        ),
        migrations.AddField(
            model_name='pointscore',
            name='done',
            field=models.BooleanField(db_column='Done', default=0),
        ),
        migrations.AddField(
            model_name='pointscore',
            name='governorate_id',
            field=models.IntegerField(db_column='Governerate', default=0),
        ),
    ]
