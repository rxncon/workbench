# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-11 13:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Graph_from_File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=120)),
                ('slug', models.SlugField(blank=True)),
                ('comment', models.TextField(blank=True, null=True)),
                ('graph_file', models.FileField(null=True, upload_to='')),
                ('graph_string', models.TextField(null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-updated', '-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='Graph_from_Quick',
            fields=[
                ('graph_from_file_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='graphs.Graph_from_File')),
            ],
            bases=('graphs.graph_from_file',),
        ),
    ]
