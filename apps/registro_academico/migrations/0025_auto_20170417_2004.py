# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-04-17 20:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registro_academico', '0024_auto_20170417_1956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='franja',
            name='nombre',
            field=models.CharField(max_length=50),
        ),
    ]