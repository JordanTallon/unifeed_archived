# Generated by Django 4.2.10 on 2024-02-19 13:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_user_track_analytics'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='track_analytics',
            new_name='track_history',
        ),
    ]