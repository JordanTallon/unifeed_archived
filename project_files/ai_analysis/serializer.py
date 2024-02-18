from rest_framework import serializers
from .models import ArticleAnalysisResults


class ArticleAnalysisResultsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ArticleAnalysisResults
        fields = ('url', 'article_text_md5', 'status',
                  'sentence_results')
