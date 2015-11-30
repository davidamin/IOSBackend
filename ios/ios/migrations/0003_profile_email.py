# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ios', '0002_auto_20151123_2355'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='email',
            field=models.EmailField(default='dma3fq@virginia.edu', max_length=254),
            preserve_default=False,
        ),
    ]
