# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-04-05 16:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registro_academico', '0013_auto_20170405_1620'),
    ]

    operations = [
        migrations.AlterField(
            model_name='citacion',
            name='idioma',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='registro_academico.Idioma'),
        ),
    ]
