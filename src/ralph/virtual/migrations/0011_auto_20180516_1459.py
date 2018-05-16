# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('virtual', '0010_auto_20180510_1504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cloudprovider',
            name='sync_event_processor',
            field=models.ForeignKey(null=True, blank=True, to='virtual.CloudSyncProcessor'),
        ),
    ]
