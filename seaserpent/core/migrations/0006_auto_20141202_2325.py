# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20141201_2254'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='last_price',
            field=models.FloatField(default=0.0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='price_difference',
            field=models.FloatField(default=0.0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.FloatField(default=0.0),
            preserve_default=True,
        ),
    ]
