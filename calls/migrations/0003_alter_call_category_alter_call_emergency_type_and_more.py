# Generated by Django 5.1.6 on 2025-02-18 03:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calls', '0002_rename_created_at_call_timestamp_call_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='call',
            name='category',
            field=models.CharField(blank=True, default='GENERAL', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='call',
            name='emergency_type',
            field=models.CharField(blank=True, choices=[('POLICE', 'Police'), ('MEDICAL', 'Medical')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='call',
            name='incident_number',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='call',
            name='location',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='call',
            name='priority_level',
            field=models.CharField(blank=True, choices=[('STANDARD', 'Standard'), ('MEDIUM', 'Medium'), ('HIGH', 'High')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='callinteraction',
            name='message',
            field=models.TextField(blank=True, null=True),
        ),
    ]
