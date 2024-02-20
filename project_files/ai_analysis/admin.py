from django.contrib import admin
from .models import ArticleAnalysisResults, AIAnalysisFeedback

# Register your models here.
admin.site.register(ArticleAnalysisResults)
admin.site.register(AIAnalysisFeedback)
