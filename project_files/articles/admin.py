from django.contrib import admin
from .models import Article, SavedArticle, RecentlyRead

admin.site.register(Article)
admin.site.register(SavedArticle)
admin.site.register(RecentlyRead)
