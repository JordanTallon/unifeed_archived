from django.db import models
from jsonfield import JSONField


class PoliticalBiasAnalysis(models.Model):
    article_url = models.URLField(max_length=200)

    # Stores the article text as a md5 hash
    article_text_md5 = models.CharField(max_length=32)

    biased_sentences = models.JSONField(default=dict)

    class Meta:
        # Override default admin display "Political bias analysiss" which is incorrect / ugly
        verbose_name_plural = "Political Bias Analysis Records"
