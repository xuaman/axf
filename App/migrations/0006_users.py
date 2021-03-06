# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-09-28 08:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0005_goods'),
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('u_name', models.CharField(max_length=128, unique=True)),
                ('u_passwd', models.CharField(max_length=128)),
                ('u_email', models.EmailField(max_length=128, unique=True)),
                ('u_icon', models.ImageField(upload_to='icons/%Y/%m/%d')),
                ('u_active', models.BooleanField(default=False)),
                ('u_delete', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'axf_users',
            },
        ),
    ]
