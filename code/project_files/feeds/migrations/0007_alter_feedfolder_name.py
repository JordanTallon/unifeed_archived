# Generated by Django 4.2.10 on 2024-02-19 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0006_feed_publisher'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedfolder',
            name='name',
            field=models.CharField(max_length=18),
        ),
    ]
