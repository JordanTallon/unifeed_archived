# Generated by Django 5.0.1 on 2024-01-29 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ai_analysis', '0002_alter_politicalbiasanalysis_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='politicalbiasanalysis',
            name='political_bias',
        ),
        migrations.AddField(
            model_name='politicalbiasanalysis',
            name='biased_sentences',
            field=models.JSONField(default=dict),
        ),
    ]
