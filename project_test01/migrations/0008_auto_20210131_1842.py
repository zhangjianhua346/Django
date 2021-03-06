# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2021-01-31 10:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project_test01', '0007_tstudent'),
    ]

    operations = [
        migrations.CreateModel(
            name='RClass',
            fields=[
                ('c_id', models.AutoField(primary_key=True, serialize=False)),
                ('cname', models.CharField(max_length=18)),
            ],
        ),
        migrations.CreateModel(
            name='RStudent',
            fields=[
                ('s_id', models.AutoField(primary_key=True, serialize=False)),
                ('sname', models.CharField(max_length=8)),
                ('score', models.PositiveIntegerField()),
                ('cls', models.ForeignKey(default=False, on_delete=django.db.models.deletion.CASCADE, to='project_test01.RClass')),
            ],
        ),
        migrations.RemoveField(
            model_name='tstudent',
            name='is_deleter',
        ),
        migrations.AddField(
            model_name='tstudent',
            name='is_delete',
            field=models.BooleanField(default=False),
        ),
    ]
