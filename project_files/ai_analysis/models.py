from django.db import models
from jsonfield import JSONField


# This object is returned instantly to the user when they make a post request to analyze the bias of an article.
# For example: the user submits a request, An instance of this model is created and returned to them with an initial processing status.
# The client reads the status as "processing" so it begins to periodically make fetch requests until the status
# is either "complete" where they will then be presented with the results or "failed" where an error message will appear.
class ArticleAnalysisResults(models.Model):
    url = models.URLField(max_length=500)

    # Stores the article text as a md5 hash
    article_text_md5 = models.CharField(max_length=32)

    # Will store each analyzed sentence and their bias values
    sentence_results = models.JSONField(default=dict)

    # Status keeps track of the asynchronous process stages to determine if the results are ready
    status = models.CharField(max_length=10, default="processing")
