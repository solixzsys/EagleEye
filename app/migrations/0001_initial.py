# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('country_code', models.CharField(serialize=False, max_length=200, default='2015-11-10 12:09:54.128593', primary_key=True)),
                ('country_name', models.CharField(max_length=200)),
                ('continent', models.CharField(max_length=200)),
            ],
        ),
    ]
