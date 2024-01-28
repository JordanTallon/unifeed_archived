from django.db import models
import hashlib


class PoliticalBiasAnalysis(models.Model):
    article_url = models.URLField(max_length=200)

    # Stores the article text as a md5 hash
    article_text_md5 = models.CharField(max_length=32)
    political_bias = models.IntegerField()

    # Function to assign the article_text_md5 hash based on the article text (using Python hashlib)
    def article_text_to_md5_hash(self, article_text):
        # Encode article text
        encoded_text = article_text.encode()
        # Convert to md5 hash
        md5_hash_result = hashlib.md5(encoded_text)
        # Digest the hash as hexadecimal and assign it to article_text_md5
        self.article_text_md5 = md5_hash_result.hexdigest()

    class Meta:
        # Override default admin display "Political bias analysiss" which is incorrect / ugly
        verbose_name_plural = "Political Bias Analysis Records"
