# Generated by Django 4.2.10 on 2024-02-18 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ai_analysis', '0007_delete_biasanalysis_articleanalysisresults_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='articleanalysisresults',
            name='sentence_html',
            field=models.JSONField(default=dict),
        ),
    ]
