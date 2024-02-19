from django.urls import path
from . import views

urlpatterns = [
    path('view/<int:article_id>/', views.article_details, name='article_details'),
    path('reading_list/', views.saved_articles, name="reading_list")
]
