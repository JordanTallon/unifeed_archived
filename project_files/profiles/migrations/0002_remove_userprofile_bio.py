# Generated by Django 5.0.1 on 2024-02-04 17:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='bio',
        ),
    ]
