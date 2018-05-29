# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_cryptography.fields


class Migration(migrations.Migration):

    dependencies = [
        ('virtual', '0011_auto_20180516_1459'),
    ]

    operations = [
        migrations.AddField(
            model_name='cloudprovider',
            name='client_config',
            field=django_cryptography.fields.encrypt(models.TextField(blank=True, null=True)),
        ),
    ]
