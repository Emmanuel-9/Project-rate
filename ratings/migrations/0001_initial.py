# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2020-08-17 15:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_pic', models.ImageField(upload_to='media/')),
                ('user_bio', models.TextField()),
                ('projects', models.TextField()),
                ('contact', models.TextField(blank=True)),
            ],
        ),
    ]
