# Generated by Django 5.0.1 on 2024-01-25 15:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('folder_system', '0001_initial'),
        ('rss_app', '0002_feeditem_delete_feed'),
    ]

    operations = [
        migrations.AddField(
            model_name='feeditem',
            name='folder',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='folder_system.folder'),
        ),
    ]