# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-05-06 15:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mapdata', '0055_auto_20170505_1334'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Area',
            new_name='Space',
        ),
        migrations.AlterField(
            model_name='lineobstacle',
            name='area',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lineobstacles', to='mapdata.Space', verbose_name='space'),
        ),
        migrations.AlterField(
            model_name='obstacle',
            name='area',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='obstacles', to='mapdata.Space', verbose_name='space'),
        ),
        migrations.AlterField(
            model_name='stair',
            name='area',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stairs', to='mapdata.Space', verbose_name='space'),
        ),
        migrations.AlterField(
            model_name='stuffedarea',
            name='area',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stuffedareas', to='mapdata.Space', verbose_name='space'),
        ),
    ]
