from django.contrib import admin
from .models import Article, SavedArticle

admin.site.register(Article)
admin.site.register(SavedArticle)
