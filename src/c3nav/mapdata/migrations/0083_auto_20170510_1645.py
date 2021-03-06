# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-10 16:45
from __future__ import unicode_literals

from django.db import migrations


def copy_locationgroups(apps, schema_editor):
    LegacyLocationGroup = apps.get_model('mapdata', 'LegacyLocationGroup')
    LocationGroup = apps.get_model('mapdata', 'LocationGroup')
    for legacyobj in LegacyLocationGroup.objects.all():
        obj = LocationGroup()
        obj.slug = legacyobj.locationslug_ptr.slug
        slug_ptr = legacyobj.locationslug_ptr
        slug_ptr.slug = None
        slug_ptr.save()
        obj.titles = legacyobj.titles
        obj.can_search = legacyobj.can_search
        obj.can_describe = legacyobj.can_describe
        obj.color = legacyobj.color
        obj.public = legacyobj.public
        obj.compiled_room = legacyobj.compiled_room
        obj.save()
        obj.arealocations.add(*legacyobj.arealocations.all())


class Migration(migrations.Migration):

    dependencies = [
        ('mapdata', '0082_auto_20170510_1644'),
    ]

    operations = [
        migrations.RunPython(copy_locationgroups),
    ]
