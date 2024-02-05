from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='feed-list'),
    path('feeds/<int:folder_id>/', views.feeds_in_folder, name='feeds_in_folder'),
    path('delete/<int:feed_id>/', views.delete_feed, name='delete_feed'),
    path('clear_all/', views.clear_all_feeds, name='clear_all_feeds'),
    path('rss', views.RssView.as_view(), name='rss'),
]

