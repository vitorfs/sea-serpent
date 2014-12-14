# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_product_price_changes'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='price_percentage_change',
            field=models.FloatField(default=0.0),
            preserve_default=True,
        ),
    ]
