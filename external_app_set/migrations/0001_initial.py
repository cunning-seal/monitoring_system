# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExternalApp',
            fields=[
                ('id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('name', models.TextField()),
            ],
        ),
    ]
