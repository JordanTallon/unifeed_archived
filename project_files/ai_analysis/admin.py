from django.contrib import admin
from .models import ArticleAnalysisResults, BiasAnalysis

# Register your models here.
admin.site.register(ArticleAnalysisResults)
admin.site.register(BiasAnalysis)
