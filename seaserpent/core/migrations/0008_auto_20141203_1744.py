# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20141202_2333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_key',
            field=models.CharField(max_length=255),
            preserve_default=True,
        ),
    ]
