# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('virtual', '0009_auto_20170522_0745'),
    ]

    operations = [
        migrations.CreateModel(
            name='CloudSyncProcessor',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('module', models.CharField(max_length=250)),
            ],
            options={
                'verbose_name': 'Cloud sync processor',
                'verbose_name_plural': 'Cloud sync processors',
            },
        ),
        migrations.AddField(
            model_name='cloudprovider',
            name='sync_enabled',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='cloudprovider',
            name='sync_event_processor',
            field=models.ForeignKey(to='virtual.CloudSyncProcessor', null=True),
        ),
    ]
