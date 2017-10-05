# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-06-22 13:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Rxncon_system',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=120)),
                ('project_id', models.IntegerField()),
                ('project_type', models.CharField(max_length=5)),
                ('slug', models.SlugField(blank=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('pickled_system', models.BinaryField()),
            ],
        ),
    ]
