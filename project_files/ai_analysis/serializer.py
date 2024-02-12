from rest_framework import serializers
from .models import ArticleAnalysisResults, BiasAnalysis


class ArticleAnalysisResultsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ArticleAnalysisResults
        fields = ('url', 'article_text_md5', 'sentence_results')


class BiasAnalysisSerializer(serializers.ModelSerializer):

    class Meta:
        model = BiasAnalysis
        fields = ('url', 'status')
