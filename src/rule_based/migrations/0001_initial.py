# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2018-06-27 12:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Rule_based_from_rxnconsys',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=120)),
                ('slug', models.SlugField(blank=True)),
                ('comment', models.TextField(blank=True, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('model_path', models.FileField(null=True, upload_to='')),
            ],
            options={
                'ordering': ['-updated', '-timestamp'],
            },
        ),
    ]
