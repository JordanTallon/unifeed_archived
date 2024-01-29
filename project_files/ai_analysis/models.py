from django.db import models
from jsonfield import JSONField
from scraper.utils import scrape_data
from utils import text_to_md5_hash, analyze_political_bias


class PoliticalBiasAnalysis(models.Model):
    article_url = models.URLField(max_length=200)

    # Stores the article text as a md5 hash
    article_text_md5 = models.CharField(max_length=32)

    article_text = models.TextField()

    biased_sentences = models.JSONField()

    @classmethod
    def create(cls, article_url):

        article_text = scrape_data(article_url)

        article_text_md5 = text_to_md5_hash(article_text)

        biased_sentences = analyze_political_bias(article_text)

        return cls(article_text=article_text, article_text_md5=article_text_md5, biased_sentences=biased_sentences)

    class Meta:
        # Override default admin display "Political bias analysiss" which is incorrect / ugly
        verbose_name_plural = "Political Bias Analysis Records"
