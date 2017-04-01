# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-03-24 14:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inscripcion', '0027_auto_20170324_1414'),
    ]

    operations = [
        migrations.AddField(
            model_name='persona',
            name='email_acudiente',
            field=models.EmailField(default='daga9420@gmail.com', max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='persona',
            name='nombre_acudiente',
            field=models.CharField(default='Daniel', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='persona',
            name='telefono_acudiente',
            field=models.BigIntegerField(default=3163431036),
            preserve_default=False,
        ),
    ]