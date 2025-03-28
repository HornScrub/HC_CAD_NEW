# Generated by Django 5.1.6 on 2025-03-26 17:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calls', '0005_remove_callinteraction_call_and_more'),
        ('incidents', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='call',
            name='incident',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='calls', to='incidents.incident'),
        ),
        migrations.DeleteModel(
            name='CallInteraction',
        ),
    ]
