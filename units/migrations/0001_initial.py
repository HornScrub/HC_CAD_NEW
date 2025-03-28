# Generated by Django 5.1.6 on 2025-03-24 20:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('calls', '0003_alter_call_category_alter_call_emergency_type_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(max_length=10, unique=True)),
                ('name', models.CharField(max_length=50)),
                ('status', models.CharField(choices=[('10-8', 'In Service'), ('10-7', 'Out of Service'), ('10-6', 'Busy'), ('10-11', 'Traffic Stop'), ('10-97', 'On Scene'), ('10-23', 'Arrived at Location'), ('10-19', 'Returning to Station')], default='10-8', max_length=10)),
                ('location', models.CharField(blank=True, max_length=100, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('current_call', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='calls.call')),
            ],
        ),
    ]
