from django.urls import path
from . import views

urlpatterns = [
    path('import/feed', views.import_new_feed, name='import_new_feed'),
    path('import/user_feed', views.import_user_feed, name='import_new_feed')
]
