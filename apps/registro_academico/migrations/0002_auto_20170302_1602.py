# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-03-02 16:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registro_academico', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Nivel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=15)),
                ('pre_requisito', models.ManyToManyField(blank=True, related_name='_nivel_pre_requisito_+', to='registro_academico.Nivel')),
            ],
        ),
        migrations.RenameModel(
            old_name='reg_Idioma',
            new_name='Idioma',
        ),
        migrations.RenameModel(
            old_name='reg_Periodo_Academico',
            new_name='Periodo_Academico',
        ),
        migrations.RenameModel(
            old_name='reg_Sede',
            new_name='Sede',
        ),
        migrations.RemoveField(
            model_name='reg_nivel',
            name='pre_requisito',
        ),
        migrations.DeleteModel(
            name='reg_Nivel',
        ),
    ]