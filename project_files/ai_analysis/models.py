from django.db import models
from jsonfield import JSONField


class ArticleAnalysisResults(models.Model):
    url = models.URLField(max_length=500)

    # Stores the article text as a md5 hash
    article_text_md5 = models.CharField(max_length=32)

    # Will store each analyzed sentence and their bias values
    sentence_results = models.JSONField(default=dict)


# This object is returned instantly to the user when they make a request to track the asynchronous bias analysis.
# For example, the user submits a request, An instance of this model is created and returned to them,
# The client reads the status as "processing" so their it begins to periodically make fetch requests until the status
# is either "complete" (where they will then be presented with a ArticleAnalysisResults object) or "failed" where an error message will appear.
class BiasAnalysis(models.Model):
    url = models.URLField(max_length=500)
    status = models.CharField(max_length=255)
