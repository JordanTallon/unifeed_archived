from rest_framework import serializers
from .models import PoliticalBiasAnalysis


class PoliticalBiasAnalysisSerializer(serializers.ModelSerializer):

    class Meta:
        model = PoliticalBiasAnalysis
        fields = ('article_url', 'article_text_md5', 'political_bias')
