from django.contrib import admin
from .models import FeedItem

class FeedItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'link')
    search_fields = ('title', 'description', 'link')
    list_filter = ('title',)

admin.site.register(FeedItem, FeedItemAdmin)
