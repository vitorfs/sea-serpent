# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20141202_2325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='last_price',
            field=models.FloatField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.FloatField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='price_difference',
            field=models.FloatField(null=True),
            preserve_default=True,
        ),
    ]
