# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2021-01-20 11:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_test01', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Film',
            fields=[
                ('id', models.IntegerField(auto_created=True, primary_key=True, serialize=False)),
                ('mname', models.CharField(max_length=32, unique=True)),
                ('mdesc', models.CharField(max_length=64)),
                ('mimg', models.CharField(max_length=32)),
                ('mlink', models.CharField(max_length=16)),
            ],
            options={
                'db_table': 'sys_film',
            },
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.IntegerField(auto_created=True, primary_key=True, serialize=False),
        ),
    ]
