# Generated by Django 5.0.1 on 2024-01-31 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ai_analysis', '0004_alter_politicalbiasanalysis_biased_sentences'),
    ]

    operations = [
        migrations.AlterField(
            model_name='politicalbiasanalysis',
            name='biased_sentences',
            field=models.JSONField(default=dict),
        ),
    ]
