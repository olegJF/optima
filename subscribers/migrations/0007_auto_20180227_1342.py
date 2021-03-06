# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-27 11:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscribers', '0006_auto_20180208_0938'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='phone',
            options={'ordering': ['number'], 'verbose_name': 'Телефон', 'verbose_name_plural': 'Телефоны'},
        ),
        migrations.RemoveField(
            model_name='phone',
            name='only_for_one',
        ),
        migrations.RemoveField(
            model_name='phone',
            name='timestamp',
        ),
        migrations.RemoveField(
            model_name='region',
            name='slug',
        ),
        migrations.AlterField(
            model_name='phone',
            name='number',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
