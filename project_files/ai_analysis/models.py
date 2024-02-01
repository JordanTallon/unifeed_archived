from django.db import models
from jsonfield import JSONField
from scraper.utils import scrape_data
from ai_analysis.utils import text_to_md5_hash, analyze_political_bias


class PoliticalBiasAnalysis(models.Model):
    article_url = models.URLField(max_length=200)

    # Stores the article text as a md5 hash
    article_text_md5 = models.CharField(max_length=32)

    biased_sentences = models.JSONField(default=dict)

    @classmethod
    def create(cls, article_url):

        # Try scrape article content from the given url
        try:
            article_text = scrape_data(article_url)
        except ValueError as e:
            # No political bias analysis can be created from a broken url But it is not a 'critical failure'
            # if this happens, so returning a None object is safe here
            # Conditional logic can be applied, like if the creation of this model returns none, display a failure message to the user.
            return None

        article_text_md5 = text_to_md5_hash(article_text)

        biased_sentences = analyze_political_bias(article_text)

        return cls(article_url=article_url, article_text_md5=article_text_md5, biased_sentences=biased_sentences)

    class Meta:
        # Override default admin display "Political bias analysiss" which is incorrect / ugly
        verbose_name_plural = "Political Bias Analysis Records"
