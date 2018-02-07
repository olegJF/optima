# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-13 12:24
from __future__ import unicode_literals
import codecs

from django.db import migrations
from os import path
from unidecode import unidecode


def load_regions(apps, _):
    Region = apps.get_model('subscribers', 'Region')
    regions = []
    with codecs.open(path.join(path.dirname(__file__), 'regions.txt'), encoding='utf-8') as f:
        for line in f.readlines():
            regions.append(Region(name=line, slug=unidecode(line).replace('-','_')))

    Region.objects.bulk_create(regions)
class Migration(migrations.Migration):

    dependencies = [
        ('subscribers', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_regions)
    ]