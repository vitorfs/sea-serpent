# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_key',
            field=models.CharField(default='', unique=True, max_length=255),
            preserve_default=False,
        ),
    ]
