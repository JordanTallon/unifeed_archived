# Generated by Django 5.0.1 on 2024-01-03 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_user_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='track_analytics',
            field=models.BooleanField(default=False),
        ),
    ]
