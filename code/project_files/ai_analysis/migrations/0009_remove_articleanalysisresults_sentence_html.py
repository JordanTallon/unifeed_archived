# Generated by Django 4.2.10 on 2024-02-18 19:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ai_analysis', '0008_articleanalysisresults_sentence_html'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articleanalysisresults',
            name='sentence_html',
        ),
    ]
