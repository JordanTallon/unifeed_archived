from django.urls import path
from . import views

urlpatterns = [
    path('view/<int:article_id>/', views.article_details, name='article_details'),
    path('saved/<int:user_id>/', views.saved_articles, name="saved_articles")
]
