# Generated by Django 4.2.10 on 2024-02-18 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0005_alter_userfeed_feed'),
    ]

    operations = [
        migrations.AddField(
            model_name='feed',
            name='publisher',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]