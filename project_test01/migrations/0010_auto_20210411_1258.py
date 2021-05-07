# Generated by Django 3.1.7 on 2021-04-11 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_test01', '0009_auto_20210404_2240'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoginFormsClassModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sname', models.CharField(max_length=32)),
                ('password', models.CharField(max_length=16)),
            ],
            options={
                'db_table': 'LoginFormsClass',
            },
        ),

    ]
