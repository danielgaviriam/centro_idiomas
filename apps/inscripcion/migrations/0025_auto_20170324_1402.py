# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-03-24 14:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inscripcion', '0024_auto_20170323_1714'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='persona',
            name='email_acudiente',
        ),
        migrations.RemoveField(
            model_name='persona',
            name='nombre_acudiente',
        ),
        migrations.RemoveField(
            model_name='persona',
            name='telefono_acudiente',
        ),
        migrations.RemoveField(
            model_name='persona',
            name='usuario',
        ),
    ]