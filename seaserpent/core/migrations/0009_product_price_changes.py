# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20141203_1744'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='price_changes',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
