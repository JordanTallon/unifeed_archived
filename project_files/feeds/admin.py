from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(FeedFolder)
admin.site.register(Feed)
admin.site.register(UserFeed)
