# Generated by Django 3.1.7 on 2021-04-11 10:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project_test01', '0010_auto_20210411_1258'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModelClassForms',
            fields=[
                ('cno', models.AutoField(primary_key=True, serialize=False)),
                ('cname', models.CharField(max_length=32, verbose_name='班级')),
            ],
            options={
                'db_table': 'ModelClassForms',
            },
        ),
        migrations.CreateModel(
            name='ModelStudentForms',
            fields=[
                ('sno', models.AutoField(primary_key=True, serialize=False)),
                ('sname', models.CharField(max_length=32, verbose_name='姓名')),
                ('pwd', models.CharField(max_length=16, verbose_name='原密码')),
                ('confirm_pwd', models.CharField(max_length=16, verbose_name='确认密码')),
                ('clazz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project_test01.modelclassforms')),
            ],
            options={
                'db_table': 'ModelStudentForms',
            },
        ),

    ]