# Generated by Django 4.2.10 on 2024-02-20 16:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ai_analysis', '0011_articleanalysisresults_bias_percent_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='AIAnalysisFeedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sentence', models.CharField(max_length=500)),
                ('bias', models.CharField(blank=True, max_length=6)),
                ('confidence', models.FloatField(default=0.0)),
                ('agree', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'sentence')},
            },
        ),
    ]
