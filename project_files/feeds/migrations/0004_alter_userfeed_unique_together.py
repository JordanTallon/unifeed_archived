# Generated by Django 5.0.1 on 2024-02-16 13:51

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0003_alter_userfeed_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='userfeed',
            unique_together={('user', 'feed', 'folder')},
        ),
    ]
