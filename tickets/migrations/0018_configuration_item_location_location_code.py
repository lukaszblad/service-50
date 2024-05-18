# Generated by Django 5.0.3 on 2024-04-09 16:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0017_user_added_on_alter_incident_opened_on'),
    ]

    operations = [
        migrations.AddField(
            model_name='configuration_item',
            name='location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tickets.location'),
        ),
        migrations.AddField(
            model_name='location',
            name='code',
            field=models.CharField(default='CA', max_length=16),
            preserve_default=False,
        ),
    ]
