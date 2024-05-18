# Generated by Django 5.0.3 on 2024-05-05 08:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0025_role_alter_incident_number_user_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='manager',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='team_manager', to='tickets.role'),
        ),
    ]
